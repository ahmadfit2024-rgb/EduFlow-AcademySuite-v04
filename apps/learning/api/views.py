# =================================================================
# apps/learning/api/views.py
# -----------------------------------------------------------------
# KEEPS THE SYSTEM INTEGRATED: This file is now fully implemented
# with the core logic for updating lesson order and learning path
# structures, directly enabling the interactive management tools
# for instructors and supervisors.
# =================================================================

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from bson import ObjectId

from apps.learning.models import Course, LearningPath
from .serializers import CourseSerializer, LearningPathSerializer

class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Courses.
    Includes custom actions for interactive content management.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated] # Basic protection, can be refined

    @action(detail=True, methods=['post'], url_path='update-lesson-order')
    def update_lesson_order(self, request, pk=None):
        """
        Receives an ordered list of lesson IDs via an HTMX request
        and updates the 'order' attribute for each lesson in the course.
        """
        course = self.get_object()
        lesson_ids_order = request.data.get('lesson_order', [])
        
        if not isinstance(lesson_ids_order, list):
            return Response({'error': 'lesson_order must be a list'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a mapping of lesson_id to its new order index
        order_map = {lesson_id: index for index, lesson_id in enumerate(lesson_ids_order)}

        # Update the order for each lesson present in the map
        for lesson in course.lessons:
            lesson_id_str = str(lesson._id)
            if lesson_id_str in order_map:
                lesson.order = order_map[lesson_id_str]
        
        # Sort the lessons array in the document based on the new order
        course.lessons.sort(key=lambda l: l.order)
        course.save()
        
        return Response({'status': 'Lesson order updated successfully'}, status=status.HTTP_200_OK)

class LearningPathViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Learning Paths.
    Includes custom actions for the visual path builder.
    """
    queryset = LearningPath.objects.all()
    serializer_class = LearningPathSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='update-structure')
    def update_structure(self, request, pk=None):
        """
        Receives an ordered list of course IDs from the Path Builder UI
        and rebuilds the 'modules' array for the learning path.
        """
        learning_path = self.get_object()
        course_ids = request.data.get('course_ids', [])
        
        if not isinstance(course_ids, list):
            return Response({'error': 'course_ids must be a list'}, status=status.HTTP_400_BAD_REQUEST)

        # Rebuild the modules array with the correct structure and order
        new_modules = []
        for index, course_id in enumerate(course_ids):
            # Ensure the course actually exists before adding it
            if Course.objects.filter(pk=course_id).exists():
                module_instance = {'course_id': course_id, 'order': index}
                new_modules.append(module_instance)
        
        learning_path.modules = new_modules
        learning_path.save()

        return Response({'status': 'Learning path structure updated successfully'}, status=status.HTTP_200_OK)