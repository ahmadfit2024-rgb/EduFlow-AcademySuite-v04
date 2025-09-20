# =================================================================
# apps/interactions/api/views.py
# -----------------------------------------------------------------
# KEEPS THE SYSTEM INTEGRATED: This file creates the backend API
# endpoint for the AI Assistant, fulfilling a core feature from the
# project's functional specification.
# =================================================================

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from .serializers import AIQuestionSerializer
from apps.interactions.services import AIAssistantService
from apps.learning.models import Course, Lesson

class AIAssistantApiView(APIView):
    """
    API View to handle questions directed to the AI Assistant.
    It ensures the user is authenticated and then fetches a context-aware
    answer from the AI service.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # 1. Validate the incoming data format
        serializer = AIQuestionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        question = validated_data['question']
        course_id = validated_data['course_id']
        lesson_id = validated_data['lesson_id']

        try:
            # 2. Build the context for the AI model
            # This is a critical step to get relevant answers.
            course = get_object_or_404(Course, pk=course_id)
            lesson = next((l for l in course.lessons if str(l._id) == lesson_id), None)
            
            if not lesson:
                return Response({'error': 'Lesson not found in this course.'}, status=status.HTTP_404_NOT_FOUND)

            context = {
                "course_title": course.title,
                "lesson_title": lesson.title,
                # For now, we pass the description. This can be expanded to include full text content.
                "lesson_content": lesson.content_data.get('description', 'No textual content available for this lesson.')
            }

            # 3. Call the AI service to get the answer
            ai_service = AIAssistantService()
            answer = ai_service.get_answer(question=question, context=context)
            
            # 4. Return the answer in the expected JSON format for HTMX
            return Response({'answer': answer}, status=status.HTTP_200_OK)

        except Exception as e:
            # General error handling for unexpected issues
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)