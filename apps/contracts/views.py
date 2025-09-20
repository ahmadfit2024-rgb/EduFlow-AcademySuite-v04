# =================================================================
# apps/contracts/views.py
# -----------------------------------------------------------------
# KEEPS THE SYSTEM INTEGRATED: This view is now fully functional.
# It performs a security check, gathers real enrollment data for all
# students under a specific contract, and uses the Excel service
# to generate a secure, downloadable report for the client.
# =================================================================

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Avg

from .models import Contract
from apps.enrollment.models import Enrollment
from apps.reports.services.excel_generator import ExcelReportGenerator
from apps.users.models import CustomUser

class ExportContractReportView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Handles the request to export a contract's employee progress report as an Excel file.
    """
    def test_func(self):
        # Security check: Ensure only the client of the contract or an admin can download
        contract = get_object_or_404(Contract, pk=self.kwargs['pk'])
        return self.request.user.role == CustomUser.Roles.ADMIN or self.request.user == contract.client
    
    def get(self, request, *args, **kwargs):
        contract = get_object_or_404(Contract, pk=self.kwargs['pk'])
        
        # --- Data Gathering Logic (Live Data) ---
        # Get all students associated with this contract
        enrolled_students_qs = contract.enrolled_students.all()
        student_ids = enrolled_students_qs.values_list('id', flat=True)
        
        # Get all their enrollments
        all_enrollments = Enrollment.objects.filter(student_id__in=student_ids)
        
        report_data = []
        for student in enrolled_students_qs:
            # Calculate the average progress for this specific student across all their enrollments
            avg_progress = all_enrollments.filter(student=student).aggregate(Avg('progress'))['progress__avg'] or 0
            
            report_data.append({
                'student_name': student.full_name or student.username,
                'student_email': student.email,
                'enrollment_date': student.date_joined.strftime("%Y-%m-%d"), # Approximation of enrollment date
                'progress': f"{avg_progress:.2f}", # Format to 2 decimal places
                'status': 'Completed' if avg_progress >= 100 else 'In Progress',
            })
        
        # --- Generate and Return Excel File ---
        report_title = f"Contract_{contract.title.replace(' ', '_')}"
        generator = ExcelReportGenerator()
        return generator.generate_course_enrollment_excel(report_title, report_data)