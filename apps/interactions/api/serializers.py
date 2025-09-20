from rest_framework import serializers

class AIQuestionSerializer(serializers.Serializer):
    """
    Serializer for validating the incoming AI assistant question.
    """
    question = serializers.CharField(max_length=1000)
    course_id = serializers.CharField(max_length=24)
    lesson_id = serializers.CharField(max_length=24)