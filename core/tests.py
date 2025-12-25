from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Event, Alert


class ThreatSystemTests(APITestCase):
    """
    Integration and behavior tests for the Threat Alert System.

    Scope:
    - Event ingestion
    - Automatic alert creation via signals
    - Role-based access control
    - API authorization & permissions

    Test users:
    - analyst (regular user)
    - admin_user (superuser)
    """

    def setUp(self):
        """
        Set up test users and commonly used API endpoints.
        """
        self.user = User.objects.create_user(
            username='analyst', password='password123')
        self.admin = User.objects.create_superuser(
            username='admin_user', password='password123')
        self.ingest_url = reverse('event-ingest')
        self.alert_list_url = reverse('alert-list')

    def test_high_severity_creates_alert(self):
        """
        Ensure an Alert is automatically created when
        a HIGH severity Event is created.
        """
        event = Event.objects.create(
            source="Test-Sensor",
            event_type="Malware",
            severity="HIGH",
            description="Testing automatic alert generation."
        )
        self.assertTrue(Alert.objects.filter(event=event).exists())

    def test_low_severity_no_alert(self):
        """
        Ensure no Alert is created for LOW severity Events.
        """
        event = Event.objects.create(
            source="Test-Sensor",
            event_type="Ping",
            severity="LOW",
            description="Just a routine check."
        )
        self.assertFalse(Alert.objects.filter(event=event).exists())

    def test_create_event_api(self):
        """
        Verify authenticated users can create Events via API
        and CRITICAL severity triggers Alert creation.
        """
        self.client.force_authenticate(user=self.user)
        data = {
            "source": "API-Tester",
            "event_type": "DDoS",
            "severity": "CRITICAL",
            "description": "Critical traffic spike detected via API."
        }
        response = self.client.post(self.ingest_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Alert.objects.count(), 1)

    def test_unauthorized_access(self):
        """
        Ensure unauthenticated users cannot access alert list API.
        """
        self.client.logout()
        response = self.client.get(self.alert_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_analyst_cannot_update_alert(self):
        """
        Ensure non-admin users (analysts) are forbidden
        from updating Alert status.
        """
        event = Event.objects.create(
            source="Test",
            severity="HIGH",
            description="Test"
        )
        alert = Alert.objects.get(event=event)
        self.client.force_authenticate(user=self.user)
        update_url = reverse('alert-update', args=[alert.id])
        response = self.client.patch(update_url, {"status": "RESOLVED"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
