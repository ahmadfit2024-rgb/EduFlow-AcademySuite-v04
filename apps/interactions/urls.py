# =================================================================
# apps/interactions/urls.py
# -----------------------------------------------------------------
# KEEPS THE SYSTEM INTEGRATED: A new URL for adding a post (reply)
# is added. This is essential for the reply form to submit to the
# correct backend endpoint.
# =================================================================

from django.urls import path
from .views import AddDiscussionThreadView, AIChatFormView, AddDiscussionPostView

app_name = 'interactions'

urlpatterns = [
    path('lessons/<str:lesson_id>/add-thread/', AddDiscussionThreadView.as_view(), name='add_thread'),
    path('ai-chat-form/course/<str:course_pk>/lesson/<str:lesson_id>/', AIChatFormView.as_view(), name='ai_chat_form'),
    
    # New URL to handle posting a reply to a thread.
    # The HTMX form in the template will point to this URL.
    path('threads/<str:thread_id>/add-post/', AddDiscussionPostView.as_view(), name='add_post'),
]