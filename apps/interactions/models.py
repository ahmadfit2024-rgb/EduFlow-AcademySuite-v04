from djongo import models
from django.conf import settings

class DiscussionThread(models.Model):
    """
    Represents a discussion thread related to a specific lesson.
    """
    _id = models.ObjectIdField()
    lesson_id = models.CharField(max_length=24) # Refers to a lesson inside a Course document
    course_id = models.CharField(max_length=24) # Refers to the course document
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.DjongoManager()

    def __str__(self):
        return self.title

class DiscussionPost(models.Model):
    """
    Represents a single reply within a discussion thread.
    """
    _id = models.ObjectIdField()
    thread = models.ForeignKey(DiscussionThread, on_delete=models.CASCADE, related_name='posts')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reply_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.DjongoManager()

    def __str__(self):
        return f"Reply by {self.user.username} on {self.thread.title}"