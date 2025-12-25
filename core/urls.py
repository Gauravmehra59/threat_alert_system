from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from .views import (
    EventCreateView,
    AlertListView,
    AlertUpdateView,
)

urlpatterns = [
    # Event Ingestion
    path(
        'event/ingest/',
        EventCreateView.as_view(),
        name='event-ingest'
    ),

    # Alert Management
    path(
        'alerts/',
        AlertListView.as_view(),
        name='alert-list'
    ),

    # Specific Alert Update
    path(
        'alerts/<int:pk>/',
        AlertUpdateView.as_view(),
        name='alert-update'
    ),

    # Login API
    path(
        'auth/login/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),

    path(
        'auth/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]
