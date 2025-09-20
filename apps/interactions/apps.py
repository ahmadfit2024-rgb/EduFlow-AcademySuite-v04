# =================================================================
# apps/interactions/apps.py
# -----------------------------------------------------------------
# KEEPS THE SYSTEM INTEGRATED: This file is updated to import and
# register the new signals.py file. This is a critical step to
# ensure that the webhook signals are active when the app runs.
# =================================================================

from django.apps import AppConfig

class InteractionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.interactions'

    def ready(self):
        # This line is essential for the signals to be discovered and used by Django.
        import apps.interactions.signals