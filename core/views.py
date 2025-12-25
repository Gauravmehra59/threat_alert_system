from rest_framework import generics, permissions, filters
from .models import Event, Alert
from django_filters.rest_framework import DjangoFilterBackend
from . serializers import (
    EventSerializer,
    AlertSerializer,
    AlertUpdateSerializer
)


class EventCreateView(generics.CreateAPIView):
    """
    API endpoint for ingesting security events.

    Purpose:
    - Allows authenticated users to create new Event records.
    - Triggers post_save signals for automatic Alert creation
      based on severity (HIGH / CRITICAL).

    Permissions:
    - Authenticated users only.

    Method:
    - POST /event/ingest/
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]


class AlertListView(generics.ListAPIView):
    """
    API endpoint to list and query generated Alerts.

    Purpose:
    - Provides visibility into system-generated alerts.
    - Supports filtering and ordering for operational monitoring.

    Permissions:
    - Authenticated users only.

    Filtering:
    - status (Alert status)
    - event__severity (related Event severity)

    Ordering:
    - created_at (ascending / descending)

    Method:
    - GET /alerts/
    """
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'event__severity']
    ordering_fields = ['created_at']


class AlertUpdateView(generics.UpdateAPIView):
    """
    API endpoint to update Alert status.

    Purpose:
    - Allows administrative users to modify alert state
      (e.g., OPEN → RESOLVED).

    Permissions:
    - Admin users only.

    Allowed updates:
    - status field only.

    Method:
    - PATCH /alerts/<id>/
    """
    queryset = Alert.objects.all()
    serializer_class = AlertUpdateSerializer
    permission_classes = [permissions.IsAdminUser]
