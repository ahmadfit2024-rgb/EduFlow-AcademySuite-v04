# =================================================================
# apps/users/models.py
# -----------------------------------------------------------------
# KEEPS THE SYSTEM INTEGRATED: A `__str__` method is added to
# return the user's full name. This is a small but critical UX
# improvement that makes user selection dropdowns and admin displays
# far more readable and professional.
# =================================================================

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        SUPERVISOR = 'supervisor', 'Supervisor'
        INSTRUCTOR = 'instructor', 'Instructor'
        STUDENT = 'student', 'Student'
        THIRD_PARTY = 'third_party', 'Third-Party Client'

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.STUDENT,
        help_text="The role of the user within the system."
    )
    full_name = models.CharField(
        max_length=255, 
        blank=True, 
        help_text="User's full name."
    )
    avatar_url = models.URLField(
        blank=True, 
        null=True, 
        help_text="URL for the user's profile picture."
    )

    def save(self, *args, **kwargs):
        if not self.full_name and (self.first_name or self.last_name):
            self.full_name = f"{self.first_name} {self.last_name}".strip()
        super().save(*args, **kwargs)

    def __str__(self):
        # If full_name is available, use it for a more human-readable representation.
        return self.full_name or self.username