"""
patients/urls.py
~~~~~~~~~~~~~~~~
Defines URL patterns for patient management endpoints including
CRUD operations, search, ordering, and pagination.
Connects the PatientViewSet with DRF routers.
"""

from django.urls import path
from .views import PatientViewSet


urlpatterns = [
    path(
        '/<int:pk>',
        PatientViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }), name='patient-detail'),

    path(
        '',
        PatientViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='patient-list'),
]
