from django.contrib import admin
from .models import DiscussionThread, DiscussionPost

@admin.register(DiscussionThread)
class DiscussionThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'course_id', 'lesson_id', 'created_at')
    search_fields = ('title', 'question')

@admin.register(DiscussionPost)
class DiscussionPostAdmin(admin.ModelAdmin):
    list_display = ('thread', 'user', 'created_at')
    search_fields = ('reply_text',)