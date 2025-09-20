# =================================================================
# apps/reports/views.py
# -----------------------------------------------------------------
# KEEPS THE SYSTEM INTEGRATED: This view is now fully functional.
# It fetches real data for the report filters and processes form
# submissions by calling the generator services with live, queried
# data from the database, replacing all placeholder logic.
# =================================================================

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages

from .services.pdf_generator import PDFReportGenerator
from .services.excel_generator import ExcelReportGenerator
from apps.users.models import CustomUser
from apps.learning.models import Course
from apps.enrollment.models import Enrollment

class ReportDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    A view that displays the reporting dashboard and allows authorized
    users to select and generate different types of reports.
    """
    template_name = "reports/report_dashboard.html"

    def test_func(self):
        # Only Admins and Supervisors can access the reporting dashboard
        return self.request.user.role in [CustomUser.Roles.ADMIN, CustomUser.Roles.SUPERVISOR]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Reporting Dashboard"
        # Provide real data to the template for filter dropdowns
        context["students"] = CustomUser.objects.filter(role=CustomUser.Roles.STUDENT)
        context["courses"] = Course.objects.all()
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        report_type = request.POST.get("report_type")

        if report_type == "student_pdf":
            student_id = request.POST.get("student_id")
            course_id = request.POST.get("course_id")
            
            if not student_id or not course_id:
                messages.error(request, "Please select both a student and a course.")
                return HttpResponseRedirect(reverse('reports:report_dashboard'))

            student = get_object_or_404(CustomUser, id=student_id)
            course = get_object_or_404(Course, pk=course_id)
            enrollment = Enrollment.objects.filter(student=student, enrollable_id=str(course._id)).first()

            if not enrollment:
                messages.warning(request, f"{student} is not enrolled in '{course.title}'.")
                return HttpResponseRedirect(reverse('reports:report_dashboard'))
            
            # Prepare real data for the PDF generator
            student_data = {
                "student_name": student.full_name or student.username,
                "course_title": course.title,
                "enrollment_date": enrollment.enrollment_date.strftime("%Y-%m-%d"),
                "progress": enrollment.progress,
                "status": enrollment.get_status_display(),
            }
            generator = PDFReportGenerator()
            return generator.generate_student_performance_pdf(student_data)
        
        elif report_type == "course_excel":
            course_id = request.POST.get("course_id")
            if not course_id:
                messages.error(request, "Please select a course.")
                return HttpResponseRedirect(reverse('reports:report_dashboard'))
                
            course = get_object_or_404(Course, pk=course_id)
            enrollments = Enrollment.objects.filter(enrollable_id=str(course._id), enrollable_type='Course').select_related('student')
            
            # Prepare real data for the Excel generator
            enrollments_data = [
                {
                    'student_name': enr.student.full_name or enr.student.username,
                    'student_email': enr.student.email,
                    'enrollment_date': enr.enrollment_date.strftime("%Y-%m-%d"),
                    'progress': enr.progress,
                    'status': enr.get_status_display(),
                }
                for enr in enrollments
            ]
            generator = ExcelReportGenerator()
            return generator.generate_course_enrollment_excel(course.title, enrollments_data)

        messages.error(request, "Invalid report type selected.")
        return HttpResponseRedirect(reverse('reports:report_dashboard'))