# =================================================================
# apps/users/forms.py
# -----------------------------------------------------------------
# KEEPS THE SYSTEM INTEGRATED: The forms are updated to work
# seamlessly inside modals. The widgets are refined for better
# display, and the password field is correctly handled for the
# create vs. update scenarios.
# =================================================================

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'full_name', 'role', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if 'password' in field_name:
                 field.widget = forms.PasswordInput(attrs={'class': 'form-control'})

class CustomUserChangeForm(forms.ModelForm):
    """
    A form for updating existing users by an admin. Password is not handled here.
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'full_name', 'role', 'is_active', 'avatar_url')
        widgets = {
            'avatar_url': forms.URLInput(attrs={'placeholder': 'https://example.com/image.png'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'