from django.db import models


class SeverityLevel(models.TextChoices):
    LOW = "LOW", "Low"
    MEDIUM = "MEDIUM", "Medium"
    HIGH = "HIGH", "High"
    CRITICAL = "CRITICAL", "Critical"


class AlertStatus(models.TextChoices):
    OPEN = "OPEN", "Open"
    ACKNOWLEDGED = "ACKNOWLEDGED", "Acknowledged"
    RESOLVED = "RESOLVED", "Resolved"


class Event(models.Model):
    source = models.CharField(
        max_length=100, help_text="e.g., Firewall, CCTV, Server-1")
    event_type = models.CharField(
        max_length=100, help_text="e.g., Malware, Intrusion")
    severity = models.CharField(max_length=10, choices=SeverityLevel.choices)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source} - {self.event_type} ({self.severity})"


class Alert(models.Model):
    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        related_name="alert"
    )
    status = models.CharField(
        max_length=20,
        choices=AlertStatus.choices,
        default=AlertStatus.OPEN
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert for {self.event.source} - Status: {self.status}"
