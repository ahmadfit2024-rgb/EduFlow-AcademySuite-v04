import requests
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Enrollment
import logging

# Set up a logger for this module
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Enrollment)
def trigger_new_enrollment_webhook(sender, instance, created, **kwargs):
    """
    Sends a webhook to a predefined URL (e.g., n8n) when a new enrollment is created.
    """
    if created:
        webhook_url = os.getenv('N8N_NEW_ENROLLMENT_WEBHOOK_URL')
        
        if not webhook_url:
            logger.warning("N8N_NEW_ENROLLMENT_WEBHOOK_URL is not set. Skipping webhook.")
            return

        payload = {
            'enrollment_id': str(instance._id),
            'student_id': str(instance.student.id),
            'enrollable_id': str(instance.enrollable_id),
            'enrollable_type': instance.enrollable_type,
            'enrollment_date': instance.enrollment_date.isoformat(),
        }

        try:
            response = requests.post(webhook_url, json=payload, timeout=5)
            response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
            logger.info(f"Successfully sent webhook for enrollment ID {instance._id}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send webhook for enrollment ID {instance._id}: {e}")