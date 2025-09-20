from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """
    Customize the Django admin interface for the CustomUser model.
    """
    model = CustomUser
    list_display = ('username', 'email', 'full_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active', 'groups')
    search_fields = ('username', 'full_name', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Role & Profile', {'fields': ('role', 'full_name')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role & Profile', {'fields': ('role', 'full_name')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)