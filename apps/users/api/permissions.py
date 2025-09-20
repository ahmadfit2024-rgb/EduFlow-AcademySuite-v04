from rest_framework.permissions import BasePermission, IsAdminUser

class IsAdminRole(IsAdminUser):
    """
    Allows access only to users with the 'admin' role.
    This is more specific than IsAdminUser which checks is_staff.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')

class IsSupervisorRole(BasePermission):
    """
    Allows access only to users with the 'supervisor' role.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'supervisor')

class IsInstructorRole(BasePermission):
    """
    Allows access only to users with the 'instructor' role.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'instructor')