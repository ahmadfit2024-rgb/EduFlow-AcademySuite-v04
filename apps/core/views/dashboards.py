# =================================================================
# apps/core/views/dashboards.py
# -----------------------------------------------------------------
# KEEPS THE SYSTEM INTEGRATED: This file is updated to implement
# the full data-fetching logic for the student dashboard, fulfilling
# [cite_start]the user story defined in the foundational document[cite: 650].
# =================================================================

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count, Q
from django.urls import reverse

from apps.enrollment.models import Enrollment
from apps.learning.models import Course, LearningPath
from apps.users.models import CustomUser
from apps.contracts.models import Contract
from apps.interactions.models import DiscussionThread, DiscussionPost

class DashboardView(LoginRequiredMixin, View):
    """
    A smart view that renders the correct dashboard template
    based on the logged-in user's role and populates it with
    relevant data.
    """
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        user = request.user
        context = {'user': user}
        
        if user.role == 'admin':
            context.update({
                'total_users': CustomUser.objects.count(),
                'total_students': CustomUser.objects.filter(role=CustomUser.Roles.STUDENT).count(),
                'total_instructors': CustomUser.objects.filter(role=CustomUser.Roles.INSTRUCTOR).count(),
                'total_courses': Course.objects.count(),
            })

        elif user.role == 'student':
            # --- STUDENT DASHBOARD LOGIC - FULLY IMPLEMENTED ---
            student_enrollments = Enrollment.objects.filter(student=user).select_related('student')
            enrolled_courses_data = []
            
            for enrollment in student_enrollments:
                if enrollment.enrollable_type == 'Course':
                    try:
                        course = Course.objects.get(_id=enrollment.enrollable_id)
                        
                        # Determine the URL to continue learning
                        last_lesson_id = enrollment.last_accessed_lesson_id
                        if last_lesson_id:
                            # Find the order of the last accessed lesson
                            lesson_order = next((l.order for l in course.lessons if str(l._id) == last_lesson_id), 1)
                        else:
                            # Default to the first lesson if none accessed
                            lesson_order = 1
                            if course.lessons:
                                lesson_order = sorted(course.lessons, key=lambda l: l.order)[0].order

                        continue_url = reverse('learning:lesson_detail', kwargs={'course_slug': course.slug, 'lesson_order': lesson_order})

                        enrolled_courses_data.append({
                            'course': course,
                            'progress': enrollment.progress,
                            'continue_url': continue_url
                        })
                    except Course.DoesNotExist:
                        continue # Skip if the enrolled course is not found
            
            context['enrolled_courses_data'] = enrolled_courses_data

        elif user.role == 'instructor':
            instructor_courses = Course.objects.filter(instructor=user)
            course_ids = [str(c._id) for c in instructor_courses]
            total_students_count = Enrollment.objects.filter(enrollable_id__in=course_ids).values('student').distinct().count()

            # Logic to find unanswered questions more accurately
            # Get all threads in the instructor's courses
            course_threads = DiscussionThread.objects.filter(course_id__in=course_ids)
            # Get IDs of threads the instructor has replied to
            replied_thread_ids = DiscussionPost.objects.filter(thread__in=course_threads, user=user).values_list('thread_id', flat=True)
            # Count threads where the instructor has not replied
            unanswered_threads_count = course_threads.exclude(pk__in=replied_thread_ids).count()
            
            enrollments_per_course = Enrollment.objects.filter(enrollable_id__in=course_ids).values('enrollable_id').annotate(count=Count('student_id'))
            enrollment_map = {item['enrollable_id']: item['count'] for item in enrollments_per_course}

            for course in instructor_courses:
                course.enrolled_count = enrollment_map.get(str(course._id), 0)

            context.update({
                'instructor_courses': instructor_courses,
                'total_students': total_students_count,
                'total_courses': instructor_courses.count(),
                'new_questions_count': unanswered_threads_count,
            })

        elif user.role == 'third_party':
            try:
                contract = Contract.objects.get(client=user, is_active=True)
                student_ids = contract.enrolled_students.values_list('id', flat=True)
                enrollments = Enrollment.objects.filter(student_id__in=student_ids)
                average_progress = enrollments.aggregate(Avg('progress'))['progress__avg'] or 0
                
                employee_data = []
                for student in contract.enrolled_students.all():
                    avg_student_progress = enrollments.filter(student=student).aggregate(Avg('progress'))['progress__avg'] or 0
                    employee_data.append({
                        'name': student.full_name or student.username,
                        'email': student.email,
                        'progress': avg_student_progress,
                    })
                context.update({
                    'contract': contract,
                    'total_employees': len(student_ids),
                    'average_progress': average_progress,
                    'employee_data': employee_data,
                })
            except Contract.DoesNotExist:
                context['contract'] = None
        
        elif user.role == 'supervisor':
            context['learning_paths'] = LearningPath.objects.filter(supervisor=user)


        # Mapping and rendering logic remains the same
        dashboard_templates = {
            'admin': 'dashboards/admin.html',
            'supervisor': 'dashboards/supervisor.html',
            'instructor': 'dashboards/instructor.html',
            'student': 'dashboards/student.html',
            'third_party': 'dashboards/third_party.html',
        }
        template_name = dashboard_templates.get(user.role)
        if not template_name:
            return redirect('login')

        return render(request, template_name, context)