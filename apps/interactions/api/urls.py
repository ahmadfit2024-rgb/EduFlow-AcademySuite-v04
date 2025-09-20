# =================================================================
# apps/interactions/api/urls.py
# -----------------------------------------------------------------
# KEEPS THE SYSTEM INTEGRATED: This file defines the specific URL for
# the AI Assistant API, making the feature accessible to the frontend.
# =================================================================

from django.urls import path
from .views import AIAssistantApiView

# This is NOT an app_name for frontend URLs, but for API versioning.
app_name = 'interactions_api'

urlpatterns = [
    # This URL directly matches the endpoint defined in the foundational document.
    # It's the single point of contact for the frontend to ask the AI a question.
    path('ai-assistant/ask/', AIAssistantApiView.as_view(), name='ai_ask'),
]