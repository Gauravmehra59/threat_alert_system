from django.contrib import admin
from .models import Event, Alert


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'source',
        'event_type',
        'severity',
        'timestamp',
    )

    list_filter = (
        'severity',
        'event_type'
    )

    readonly_fields = ('timestamp',)


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = (
        'event',
        'status',
        'created_at'
    )

    list_filter = ('status',)

    readonly_fields = ('created_at',)
