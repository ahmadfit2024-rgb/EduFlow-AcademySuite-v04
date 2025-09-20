from djongo import models
from django.conf import settings

class Contract(models.Model):
    """
    Represents a B2B contract that links a third-party client to a set of 
    students and the learning paths they are entitled to access.
    """
    _id = models.ObjectIdField()
    
    title = models.CharField(max_length=255, help_text="A descriptive title for the contract, e.g., 'ABC Corp - Q4 Onboarding'.")

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT,
        related_name='contracts_as_client',
        help_text="The third-party user representing the client company."
        # limit_choices_to={'role': 'third_party'} # This can be enforced in forms/admin
    )

    enrolled_students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='contracts_as_student',
        help_text="Students covered under this contract."
        # limit_choices_to={'role': 'student'}
    )

    learning_paths = models.ManyToManyField(
        'learning.LearningPath',
        help_text="Learning paths included in this contract."
    )

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    is_active = models.BooleanField(default=True, help_text="A deactivated contract will prevent access for its students.")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.DjongoManager()

    def __str__(self):
        return self.title