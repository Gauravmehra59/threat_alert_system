from rest_framework import serializers
from .models import Event, Alert


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for the Event model.

    Purpose:
    - Used to serialize and deserialize Event data.
    - Handles full Event object representation.

    Behavior:
    - All fields are included.
    - `timestamp` field is read-only and cannot be modified via API.

    Use case:
    - Nested inside AlertSerializer
    - Event creation or retrieval APIs
    """
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['timestamp']


class AlertSerializer(serializers.ModelSerializer):
    """
    Serializer for the Alert model (Read / Detail view).

    Purpose:
    - Provides a complete representation of an Alert.
    - Includes related Event details using nested serialization.

    Behavior:
    - `event` is read-only and serialized using EventSerializer.
    - Suitable for GET/list/detail APIs.

    Fields:
    - id: Unique identifier of the alert
    - status: Current alert status
    - created_at: Alert creation timestamp (read-only)
    - event: Related Event object (nested)
    """
    event = EventSerializer()

    class Meta:
        model = Alert
        fields = [
            'id',
            'status',
            'created_at',
            'event'
        ]
        read_only_field = ['created_at']


class AlertUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating Alert status.

    Purpose:
    - Used specifically for partial updates (PATCH/PUT).
    - Restricts updates to only the `status` field.

    Behavior:
    - Prevents modification of other Alert fields.
    - Ideal for alert acknowledgment, escalation, or resolution workflows.

    Use case:
    - PATCH /alerts/<id>/
    """
    class Meta:
        model = Alert
        fields = ['status']
