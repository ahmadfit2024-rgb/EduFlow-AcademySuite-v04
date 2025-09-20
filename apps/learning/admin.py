from django.contrib import admin
from .models import Course, LearningPath

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'instructor')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = ('title', 'supervisor', 'created_at')
    list_filter = ('supervisor',)
    search_fields = ('title', 'description')