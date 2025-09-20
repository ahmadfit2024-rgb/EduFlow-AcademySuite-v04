from django.contrib import admin
from .models import Enrollment

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'enrollable_type', 'enrollable_id', 'status', 'progress', 'enrollment_date')
    list_filter = ('status', 'enrollable_type')
    search_fields = ('student__username', 'enrollable_id')