from djongo import models
from django.conf import settings
from bson import ObjectId

# --- Embedded Models for Quizzes ---

class Answer(models.Model):
    """ Embedded document for a single answer choice in a question. """
    _id = models.ObjectIdField(default=ObjectId)
    answer_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    class Meta:
        abstract = True

class Question(models.Model):
    """ Embedded document for a single quiz question. """
    _id = models.ObjectIdField(default=ObjectId)
    question_text = models.TextField()
    # Embedding the Answer model here
    answers = models.ArrayField(
        model_container=Answer,
        default=list
    )

    class Meta:
        abstract = True

# --- Main Learning Models ---

class Lesson(models.Model):
    """ Represents a single lesson within a course (Embedded). """
    _id = models.ObjectIdField(default=ObjectId)
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    content_type = models.CharField(
        max_length=20,
        choices=[
            ('video', 'Video'),
            ('pdf', 'PDF'),
            ('quiz', 'Quiz'),
            ('text_editor', 'Text Editor')
        ]
    )
    content_data = models.JSONField(default=dict)
    # When content_type is 'quiz', content_data will store an array of Question documents
    
    is_previewable = models.BooleanField(default=False)

    class Meta:
        abstract = True

class Course(models.Model):
    """ Represents a single, self-contained course. """
    _id = models.ObjectIdField()
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='courses_taught'
    )
    category = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=[('draft', 'Draft'), ('published', 'Published'), ('archived', 'Archived')],
        default='draft'
    )
    cover_image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    lessons = models.ArrayField(
        model_container=Lesson,
        default=list
    )

    objects = models.DjongoManager()

    def __str__(self):
        return self.title

class Module(models.Model):
    """ Represents a module within a Learning Path (Embedded). """
    course_id = models.CharField(max_length=24) # Storing ObjectId as string
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        abstract = True

class LearningPath(models.Model):
    """ Represents a high-level learning path or diploma. """
    _id = models.ObjectIdField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='paths_supervised'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    modules = models.ArrayField(
        model_container=Module,
        default=list
    )

    objects = models.DjongoManager()

    def __str__(self):
        return self.title