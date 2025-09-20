from rest_framework import serializers
from apps.enrollment.models import Enrollment

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'