"""
conftest.py
~~~~~~~~~~~
Reusable pytest fixtures for Patient API tests.
"""

import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from users.models import Location
from patients.models import Patient
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

@pytest.fixture
def api_client():
    """Unauthenticated DRF API client."""
    return APIClient()


@pytest.fixture
def test_user(db):
    """Test user for authentication."""
    return User.objects.create_user(username="testuser", password="testpass123")


@pytest.fixture
def auth_client(api_client, test_user):
    """Authenticated DRF API client using test_user."""
    api_client.force_authenticate(user=test_user)
    return api_client


@pytest.fixture
def location_payload():
    """Payload for creating a location."""
    return {
        "name": "Test Location",
        "address_line": "123 Main St",
        "city": "Test City",
        "state": "Test State",
        "zip_code": "12345",
        "country": "Test Country"
    }


@pytest.fixture
def test_location(db):
    """Create and return a location instance."""
    return Location.objects.create(
        name="Sample Location",
        address_line="456 Another St",
        city="Sample City",
        state="Sample State",
        zip_code="67890",
        country="Sample Country"
    )

@pytest.fixture
def patient_payload(test_user, test_location):
    """Payload for creating a patient."""
    return {
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": str(date(1990, 1, 1)),
        "gender": "Male",
        "email": "john@example.com",
        "contact_number": "1234567890",
        "place": test_location.id,
        "user": test_user.id
    }


@pytest.fixture
def patient_create(db, test_user, test_location):
    """Create and return a patient instance."""
    return Patient.objects.create(
        first_name="John",
        last_name="Doe",
        date_of_birth=date(1990, 1, 1),
        gender="Male",
        email="john@example.com",
        contact_number="1234567890",
        user=test_user,
        place=test_location
    )


@pytest.fixture
def patient_endpoints():
    """Return dictionary of patient-related endpoints with full URLs."""
    base_url = "http://localhost:8000/api/v1/patients"
    return {
        "list": f"{base_url}",
        "create": f"{base_url}",
        "detail": lambda patient_id: f"{base_url}/{patient_id}"
    }


@pytest.fixture
def payload():
    """Valid patient payload for creation."""
    return {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com",
    }
