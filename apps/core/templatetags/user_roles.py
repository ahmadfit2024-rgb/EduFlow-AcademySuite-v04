from django import template

register = template.Library()

@register.filter(name='has_role')
def has_role(user, role_name):
    """
    Checks if a user has a specific role.
    Usage: {% if request.user|has_role:'instructor' %}
    """
    return user.is_authenticated and user.role == role_name