# =================================================================
# apps/enrollment/models.py
# -----------------------------------------------------------------
# KEEPS THE SYSTEM INTEGRATED: The `update_progress` method is now
# fully implemented, providing the core business logic for tracking
# [cite_start]student progress as outlined in the system architecture[cite: 288, 382].
# =================================================================

from djongo import models
from django.conf import settings
from apps.learning.models import Course

class Enrollment(models.Model):
    _id = models.ObjectIdField()
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    enrollable_id = models.CharField(max_length=24)
    enrollable_type = models.CharField(max_length=50, choices=[('Course', 'Course'), ('LearningPath', 'LearningPath')])
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('in_progress', 'In Progress'), ('completed', 'Completed')],
        default='in_progress'
    )
    progress = models.FloatField(default=0.0)
    completed_lessons = models.JSONField(default=list) # Stores list of completed lesson_ids (as strings)
    last_accessed_lesson_id = models.CharField(max_length=24, blank=True, null=True)
    quiz_attempts = models.JSONField(default=list)
    objects = models.DjongoManager()
    
    class Meta:
        unique_together = ('student', 'enrollable_id')

    def __str__(self):
        return f"{self.student.username} enrolled in {self.enrollable_type} ({self.enrollable_id})"

    def update_progress(self):
        """
        Calculates and updates the progress percentage based on completed lessons.
        This method is now fully functional.
        """
        if self.enrollable_type == 'Course':
            try:
                course = Course.objects.get(_id=self.enrollable_id)
                total_lessons = len(course.lessons)
                
                if total_lessons > 0:
                    # Ensure completed_lessons contains unique lesson IDs
                    completed_set = set(self.completed_lessons)
                    completed_count = len(completed_set)
                    self.progress = round((completed_count / total_lessons) * 100, 2)
                else:
                    # If a course has no lessons, completing it means 100% progress.
                    self.progress = 100 if self.status == 'completed' else 0
                
                # Automatically mark the course as completed if progress is 100% or more
                if self.progress >= 100:
                    self.status = 'completed'
                    self.progress = 100 # Cap progress at 100
                
                self.save()

            except Course.DoesNotExist:
                # If course is deleted, reset progress.
                self.progress = 0
                self.save()