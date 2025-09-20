# =================================================================
# apps/interactions/templatetags/discussion_tags.py
# -----------------------------------------------------------------
# KEEPS THE SYSTEM INTEGRATED: A new template tag `get_post_form`
# is added to provide the reply form instance to the templates,
# ensuring a clean separation of concerns.
# =================================================================

from django import template
from ..models import DiscussionThread
from ..forms import DiscussionThreadForm, DiscussionPostForm

register = template.Library()

@register.simple_tag
def get_discussions_for_lesson(lesson_id):
    """ Template tag to fetch all discussion threads for a given lesson_id. """
    return DiscussionThread.objects.filter(lesson_id=str(lesson_id)).order_by('-created_at')

@register.simple_tag
def get_discussion_form():
    """ Template tag to provide an instance of the discussion form. """
    return DiscussionThreadForm()

@register.simple_tag
def get_post_form():
    """ 
    Template tag to provide an instance of the post (reply) form.
    This is used in the thread detail partial.
    """
    return DiscussionPostForm()