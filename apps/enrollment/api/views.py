# =================================================================
# apps/enrollment/api/views.py
# -----------------------------------------------------------------
# KEEPS THE SYSTEM INTEGRATED: The submit_quiz action is refined to
# handle data professionally, calculate scores accurately, and securely
# redirect the user to a unique results page, completing the quiz
# lifecycle for the student.
# =================================================================

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.urls import reverse
from bson import ObjectId
import uuid
from datetime import datetime

from apps.enrollment.models import Enrollment
from apps.learning.models import Course
from .serializers import EnrollmentSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='mark-lesson-complete')
    def mark_lesson_complete(self, request):
        user = request.user
        course_id = request.data.get('course_id')
        lesson_id = request.data.get('lesson_id')
        if not course_id or not lesson_id:
            return Response({'error': 'course_id and lesson_id are required.'}, status=status.HTTP_400_BAD_REQUEST)
        enrollment = get_object_or_404(Enrollment, student=user, enrollable_id=course_id)
        if lesson_id not in enrollment.completed_lessons:
            enrollment.completed_lessons.append(lesson_id)
        enrollment.last_accessed_lesson_id = lesson_id
        enrollment.save()
        enrollment.update_progress()
        return Response({'status': 'success', 'progress': enrollment.progress}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='submit-quiz')
    def submit_quiz(self, request):
        """
        Receives quiz answers, grades them, saves the attempt, and returns the result URL.
        """
        user = request.user
        course_id = request.data.get('course_id')
        lesson_id = request.data.get('lesson_id')
        # The form submits answers in a structure like: {'answers[question_1]': 'answer_id', ...}
        # We need to parse this into a more usable dictionary.
        answers = {key.split('[')[1].split(']')[0]: value for key, value in request.data.items() if key.startswith('answers')}

        enrollment = get_object_or_404(Enrollment, student=user, enrollable_id=course_id)
        course = get_object_or_404(Course, pk=course_id)
        lesson = next((l for l in course.lessons if str(l._id) == lesson_id), None)

        if not lesson or lesson.content_type != 'quiz':
            return Response({'error': 'Lesson is not a quiz.'}, status=status.HTTP_400_BAD_REQUEST)

        total_questions = len(lesson.content_data.get('questions', []))
        correct_answers_count = 0
        
        # Grade the submission
        for i, question_data in enumerate(lesson.content_data.get('questions', [])):
            question_key = f'question_{i+1}' # e.g., 'question_1', 'question_2'
            submitted_answer_id = answers.get(question_key)
            
            correct_answer = next((ans for ans in question_data['answers'] if ans.get('is_correct')), None)
            
            if correct_answer and submitted_answer_id == str(correct_answer.get('_id')):
                correct_answers_count += 1
        
        score = round((correct_answers_count / total_questions) * 100, 2) if total_questions > 0 else 100

        # Save the attempt with a unique ID
        attempt_id = str(uuid.uuid4())
        attempt_data = {
            'attempt_id': attempt_id,
            'lesson_id': lesson_id,
            'score': score,
            'submitted_at': datetime.utcnow().isoformat(),
            'answers': answers, # Store the submitted answers for review
        }
        
        if not hasattr(enrollment, 'quiz_attempts') or enrollment.quiz_attempts is None:
            enrollment.quiz_attempts = []
            
        enrollment.quiz_attempts.append(attempt_data)
        enrollment.save()
        
        # Construct the URL to the results page for redirection
        result_url = reverse('learning:quiz_result', kwargs={'enrollment_pk': str(enrollment._id), 'attempt_id': attempt_id})
        
        return Response({'status': 'success', 'result_url': result_url}, status=status.HTTP_200_OK)