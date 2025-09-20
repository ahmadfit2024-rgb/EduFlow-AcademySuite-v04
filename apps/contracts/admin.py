from django.contrib import admin
from .models import Contract

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    """
    Admin interface for managing B2B contracts.
    """
    list_display = ('title', 'client', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'client')
    search_fields = ('title', 'client__username', 'client__full_name')
    
    # Use filter_horizontal for a better experience with ManyToManyFields
    filter_horizontal = ('enrolled_students', 'learning_paths')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'client', 'is_active')
        }),
        ('Contract Period', {
            'fields': ('start_date', 'end_date')
        }),
        ('Entitlements', {
            'fields': ('learning_paths', 'enrolled_students')
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Filter the 'client' dropdown to only show users with the 'third_party' role
        if db_field.name == "client":
            kwargs["queryset"] = settings.AUTH_USER_MODEL.objects.filter(role='third_party')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Filter the 'enrolled_students' selector to only show users with the 'student' role
        if db_field.name == "enrolled_students":
            kwargs["queryset"] = settings.AUTH_USER_MODEL.objects.filter(role='student')
        return super().formfield_for_manytomany(db_field, request, **kwargs)