# =================================================================
# apps/interactions/signals.py (NEW FILE)
# -----------------------------------------------------------------
# KEEPS THE SYSTEM INTEGRATED: This new file defines the logic for
# sending a webhook whenever a new discussion thread is created.
# This is a core component of the project's automation strategy.
# =================================================================

import requests
import os
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DiscussionThread

# Set up a logger for this module
logger = logging.getLogger(__name__)

@receiver(post_save, sender=DiscussionThread)
def trigger_new_question_webhook(sender, instance, created, **kwargs):
    """
    Sends a webhook to a predefined URL (e.g., n8n) when a new
    discussion thread (question) is created by a student.
    """
    if created:
        webhook_url = os.getenv('N8N_QUESTION_POSTED_WEBHOOK_URL')
        
        if not webhook_url:
            logger.warning("N8N_QUESTION_POSTED_WEBHOOK_URL is not set. Skipping webhook.")
            return

        # We gather all relevant data to send a rich payload to the automation platform.
        try:
            payload = {
                'thread_id': str(instance._id),
                'student_id': str(instance.student.id),
                'student_name': instance.student.full_name or instance.student.username,
                'course_id': str(instance.course_id),
                'lesson_id': str(instance.lesson_id),
                'question_title': instance.title,
                'question_text': instance.question,
                'timestamp': instance.created_at.isoformat(),
            }

            response = requests.post(webhook_url, json=payload, timeout=10)
            # Raises an HTTPError for bad responses (4xx or 5xx)
            response.raise_for_status() 
            logger.info(f"Successfully sent 'new question' webhook for thread ID {instance._id}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send 'new question' webhook for thread ID {instance._id}: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred while sending 'new question' webhook for thread ID {instance._id}: {e}")