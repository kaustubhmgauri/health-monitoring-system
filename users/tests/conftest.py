"""
conftest.py
~~~~~~~~~~
Fixtures for API tests, including clients, users, payloads, and endpoint URLs.
"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


# -----------------------------
# API Clients
# -----------------------------
@pytest.fixture
def api_client():
    """Unauthenticated API client."""
    return APIClient()


@pytest.fixture
def test_user(db):
    """Create a regular test user."""
    return User.objects.create_user(username="testuser", password="testpass123", email="testuser@example.com")


@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    return User.objects.create_superuser(username="admin", password="adminpass123", email="admin@example.com")


@pytest.fixture
def auth_client(api_client, test_user):
    """Authenticated client as normal user."""
    api_client.force_authenticate(user=test_user)
    return api_client


@pytest.fixture
def admin_auth_client(api_client, admin_user):
    """Authenticated client as admin user."""
    api_client.force_authenticate(user=admin_user)
    return api_client


# -----------------------------
# Payloads
# -----------------------------
@pytest.fixture
def register_payload():
    return {
        "username": "newuser",
        "email": "newuser@example.com",
        "first_name": "New",
        "last_name": "User",
        "password": "newpass123",
        "password2": "newpass123"
    }


@pytest.fixture
def login_payload():
    return {
        "username": "testuser",
        "password": "testpass123"
    }


# -----------------------------
# Endpoints
# -----------------------------
@pytest.fixture
def user_endpoints():
    """
    Returns dictionary of UserViewSet endpoints with full URLs.
    """
    base_url = "http://localhost:8000/api/v1/users/auth"
    return {
        "register": f"{base_url}/register",
        "login": f"{base_url}/login",
        "list_users": f"{base_url}/list-users"
    }


@pytest.fixture
def patient_endpoints():
    """
    Returns dictionary of PatientViewSet endpoints with full URLs.
    """
    base_url = "http://localhost:8000/api/v1/patients"
    return {
        "list": f"{base_url}/",
        "create": f"{base_url}/",
        # For detail actions, format with patient_id: {base_url}/{id}/
        "detail": lambda patient_id: f"{base_url}/{patient_id}/"
    }

@pytest.fixture
def location_payload():
    """Payload for creating a location."""
    return {"name": "Test Location", "address_line": "123 Main Street"}


@pytest.fixture
def location_endpoints():
    """Return dictionary of location-related endpoints with full URLs."""
    base_url = "http://localhost:8000/api/v1/users/locations"
    return {
        "list": f"{base_url}",
        "create": f"{base_url}",
        "detail": lambda location_id: f"{base_url}/{location_id}"
    }