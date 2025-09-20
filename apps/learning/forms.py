# =================================================================
# apps/learning/forms.py
# -----------------------------------------------------------------
# KEEPS THE SYSTEM INTEGRATED: These forms are now role-aware.
# They filter the 'supervisor' and 'instructor' fields to only show
# users with the appropriate roles, preventing data entry errors and
# improving the admin/supervisor user experience.
# =================================================================

from django import forms
from .models import Course, LearningPath, Lesson
from apps.users.models import CustomUser

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title', 'slug', 'description', 'instructor', 
            'category', 'status', 'cover_image_url'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter the instructor dropdown to only show users with the 'instructor' role
        self.fields['instructor'].queryset = CustomUser.objects.filter(role=CustomUser.Roles.INSTRUCTOR)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class LearningPathForm(forms.ModelForm):
    class Meta:
        model = LearningPath
        fields = ['title', 'description', 'supervisor']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter the supervisor dropdown to only show users with the 'supervisor' role
        self.fields['supervisor'].queryset = CustomUser.objects.filter(role=CustomUser.Roles.SUPERVISOR)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class LessonForm(forms.ModelForm):
    video_url = forms.URLField(required=False, label="Video URL (Vimeo or YouTube)")
    
    class Meta:
        model = Lesson
        fields = ['title', 'content_type']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})