from rest_framework import serializers
from apps.learning.models import Course, LearningPath

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class LearningPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningPath
        fields = '__all__'