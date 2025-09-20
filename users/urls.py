"""
users/urls.py
~~~~~~~~~~~~~
Defines URL patterns for user management endpoints including
registration, login, and listing users. Integrates with
Django REST Framework ViewSets and custom actions.
"""


from django.urls import path
from .views import UserViewSet, LocationViewSet


urlpatterns = [
    path(
        "auth/register",
        UserViewSet.as_view({"post": "register"}),
        name="user-register",
    ),
    path(
        "auth/login",
        UserViewSet.as_view({"post": "login"}),
        name="user-login",
    ),
    path(
        "auth/list-users",
        UserViewSet.as_view({"get": "list_users"}),
        name="user-list-users",
    ),
    path(
        'auth/<int:pk>',
        UserViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }), name='user-detail'),

    # Location endpoints
    path(
        'locations',
        LocationViewSet.as_view({
            'get': 'list',
            'post': 'create'
        }), name='location-list'),
    
    path(
        'locations/<int:pk>',
        LocationViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }), name='location-detail'),
]

