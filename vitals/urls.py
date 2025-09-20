"""
vitals/urls.py
~~~~~~~~~~~~~~~~~
Defines URL patterns for heart rate data endpoints, including
listing, creating, retrieving, updating, and deleting heart rate
records linked to patients.
"""

from django.urls import path
from vitals.views import HeartRateViewSet


urlpatterns = [
    path(
        'heart-rates',
        HeartRateViewSet.as_view({
            'get': 'list',
            'post': 'create'
        }), name='heart-rate-list'),

    path(
        'heart-rates/<int:pk>',
        HeartRateViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }), name='heart-rate-detail'),
]