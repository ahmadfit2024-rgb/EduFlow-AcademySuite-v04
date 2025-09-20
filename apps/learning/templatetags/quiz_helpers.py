# =================================================================
# apps/learning/templatetags/quiz_helpers.py
# -----------------------------------------------------------------
# KEEPS THE SYSTEM INTEGRATED: This new file provides a custom
# template filter to simplify the logic in the quiz_result.html
# template, adhering to Django's best practice of keeping complex
# logic out of templates.
# =================================================================

from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """
    Custom template filter to allow accessing dictionary items with a
    variable key. Useful for retrieving a student's answer for a
    specific question in the quiz results page.
    Usage: {{ dictionary|get_item:key_variable }}
    """
    return dictionary.get(key)