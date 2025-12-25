from django.db.models.signals import post_save
import logging
from django.dispatch import receiver
from .models import Event, SeverityLevel, Alert

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Event)
def create_alert_signal(sender, instance, created, **kwargs):
    """
    Signal to automatically create an Alert when a high-risk Event is created.

    Trigger:
    - Fired after an Event instance is saved (post_save).

    Conditions:
    - Event must be newly created.
    - Event severity must be HIGH or CRITICAL.
    - An Alert for the Event must not already exist.

    Behavior:
    - Creates a corresponding Alert linked to the Event.
    - Logs a warning for critical operational visibility.

    Use case:
    - Automatic alert generation in Threat Monitoring Systems.
    """
    if (
        created
        and
        instance.severity in [SeverityLevel.CRITICAL, SeverityLevel.HIGH]
    ):
        if not hasattr(instance, "alert"):
            alert = Alert.objects.create(event=instance)
            logger.warning(
                f"CRITICAL ACTION: New Alert #{alert.id} generated for {instance.source} ({instance.event_type})")
