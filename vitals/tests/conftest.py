"""
conftest.py
~~~~~~~~~~
Fixtures for Patient, Location, and HeartRate API tests.
"""

import pytest
from rest_framework.test import APIClient
from users.models import User, Location
from patients.models import Patient
from vitals.models import HeartRate
from datetime import date, datetime, timedelta


# -----------------------------
# API CLIENTS
# -----------------------------
@pytest.fixture
def api_client():
    """Unauthenticated API client."""
    return APIClient()


@pytest.fixture
def auth_client(api_client, test_user):
    """Authenticated API client."""
    api_client.force_authenticate(user=test_user)
    return api_client


# -----------------------------
# TEST USER
# -----------------------------
@pytest.fixture
def test_user(db):
    """Create a test user."""
    return User.objects.create_user(username="testuser", password="testpass123")


# -----------------------------
# TEST LOCATION
# -----------------------------
@pytest.fixture
def db_location(db):
    """Create a test location."""
    return Location.objects.create(
        name="Test Location",
        address_line="123 Main St",
        city="City",
        state="State",
        zip_code="12345",
        country="Country"
    )


# -----------------------------
# TEST PATIENT
# -----------------------------
@pytest.fixture
def test_patient(db, test_user, db_location):
    """Create a patient instance."""
    return Patient.objects.create(
        user=test_user,
        first_name="John",
        last_name="Doe",
        date_of_birth=date(1990, 1, 1),
        gender="Male",
        place=db_location,
        email="johndoe@example.com",
        contact_number="1234567890"
    )


# -----------------------------
# HEART RATE PAYLOAD
# -----------------------------
@pytest.fixture
def heart_rate_payload(test_patient):
    """Payload for creating a HeartRate record."""
    return {
        "patient": test_patient.id,
        "bpm": 75,
        "recorded_at": (datetime.now() - timedelta(minutes=5)).isoformat()
    }


# -----------------------------
# HEART RATE OBJECT
# -----------------------------
@pytest.fixture
def heart_rate_create(db, test_user, test_patient):
    """Create a HeartRate record."""
    return HeartRate.objects.create(
        patient=test_patient,
        bpm=80,
        recorded_at=datetime.now(),
        recorded_by=test_user
    )


# -----------------------------
# HEART RATE ENDPOINTS
# -----------------------------
@pytest.fixture
def heart_rate_endpoints():
    """Return full URLs for HeartRate endpoints."""
    base_url = "http://localhost:8000/api/v1/vitals/heart-rates"
    return {
        "list": f"{base_url}",
        "create": f"{base_url}",
        "detail": lambda hr_id: f"{base_url}/{hr_id}"
    }
