"""
test_patient_endpoints.py
~~~~~~~~~~~~~~~~~~~~~~~~
Tests for PatientViewSet covering full CRUD, pagination, search, and ordering.
"""

import pytest
from rest_framework import status
from patients.models import Patient
from datetime import date


@pytest.mark.django_db
class TestPatientEndpoints:

    # -----------------------------
    # LIST PATIENTS
    # -----------------------------
    def test_list_patients_authenticated(self, auth_client, patient_endpoints, patient_create, settings):
        for i in range(3):
            Patient.objects.create(
                first_name=f"Patient{i}",
                last_name="Test",
                date_of_birth=date(1990, 1, i+2),
                gender="Male",
                email=f"patient{i}@example.com",
                contact_number="1234567890",
                user=auth_client.handler._force_user
            )

        settings.REST_FRAMEWORK["PAGE_SIZE"] = 2

        response = auth_client.get(patient_endpoints["list"])
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data["results"]) <= 2

    def test_list_patients_unauthenticated(self, api_client, patient_endpoints):
        response = api_client.get(patient_endpoints["list"])
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_patients_search(self, auth_client, patient_endpoints):
        Patient.objects.create(first_name="Alice", last_name="Smith", date_of_birth=date(1990,1,1),
                               gender="Female", email="alice@example.com", contact_number="111", user=auth_client.handler._force_user)
        Patient.objects.create(first_name="Bob", last_name="Builder", date_of_birth=date(1990,1,2),
                               gender="Male", email="bob@example.com", contact_number="222", user=auth_client.handler._force_user)

        response = auth_client.get(f"{patient_endpoints['list']}?search=Bob")
        assert response.status_code == status.HTTP_200_OK
        assert any(p["first_name"] == "Bob" for p in response.data["results"])

    def test_list_patients_ordering(self, auth_client, patient_endpoints):
        Patient.objects.create(first_name="Charlie", last_name="Zeta", date_of_birth=date(1990,1,3),
                               gender="Male", email="charlie@example.com", contact_number="333", user=auth_client.handler._force_user)
        Patient.objects.create(first_name="Daniel", last_name="Alpha", date_of_birth=date(1990,1,4),
                               gender="Male", email="daniel@example.com", contact_number="444", user=auth_client.handler._force_user)

        response = auth_client.get(f"{patient_endpoints['list']}?ordering=first_name")
        first_names = [p["first_name"] for p in response.data["results"]]
        assert first_names == sorted(first_names)

    # -----------------------------
    # CREATE PATIENT
    # -----------------------------
    def test_create_patient_success(self, auth_client, patient_endpoints, patient_payload):
        response = auth_client.post(patient_endpoints["create"], patient_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Patient.objects.filter(email=patient_payload["email"]).exists()

    def test_create_patient_invalid_data(self, auth_client, patient_endpoints):
        payload = {"first_name": "", "last_name": "", "email": ""}
        response = auth_client.post(patient_endpoints["create"], payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_patient_unauthenticated(self, api_client, patient_endpoints, patient_payload):
        response = api_client.post(patient_endpoints["create"], patient_payload, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # -----------------------------
    # RETRIEVE PATIENT
    # -----------------------------
    def test_retrieve_patient_success(self, auth_client, patient_endpoints, patient_create):
        url = patient_endpoints["detail"](patient_create.id)
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == patient_create.email

    def test_retrieve_patient_not_found(self, auth_client, patient_endpoints):
        url = patient_endpoints   # Non-existent ID
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    # -----------------------------
    # UPDATE PATIENT
    # -----------------------------
    def test_update_patient_success(self, auth_client, patient_endpoints, patient_create):
        url = patient_endpoints["detail"](patient_create.id)
        payload = {
            "first_name": "Updated",
            "last_name": "Name",
            "date_of_birth": str(patient_create.date_of_birth),
            "gender": patient_create.gender,
            "email": "updated@example.com",
            "contact_number": "9999999999",
            "place": patient_create.place.id,
        }
        response = auth_client.put(url, payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        patient_create.refresh_from_db()
        assert patient_create.first_name == "Updated"

    def test_update_patient_unauthenticated(self, api_client, patient_endpoints, patient_create):
        url = patient_endpoints["detail"](patient_create.id)
        payload = {"first_name": "Updated", "last_name": "Name", "email": "updated@example.com"}
        response = api_client.put(url, payload, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # -----------------------------
    # DELETE PATIENT
    # -----------------------------
    def test_delete_patient_success(self, auth_client, patient_endpoints, patient_create):
        url = patient_endpoints["detail"](patient_create.id)
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Patient.objects.filter(id=patient_create.id).exists()

    def test_delete_patient_unauthenticated(self, api_client, patient_endpoints, patient_create):
        url = patient_endpoints["detail"](patient_create.id)
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
