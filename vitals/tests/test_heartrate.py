"""
test_heartrate.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Tests for HeartRateViewSet with Patient and User integration.
"""

import pytest
from rest_framework import status
from vitals.models import HeartRate


@pytest.mark.django_db
class TestHeartRateEndpoints:

    # -----------------------------
    # LIST HEART RATES
    # -----------------------------
    def test_list_heart_rates_authenticated(self, auth_client, heart_rate_endpoints, heart_rate_create, settings):
        # Create multiple heart rate records
        for bpm in [70, 65, 85]:
            HeartRate.objects.create(
                patient=heart_rate_create.patient,
                bpm=bpm,
                recorded_at=heart_rate_create.recorded_at,
                recorded_by=heart_rate_create.recorded_by
            )

        settings.REST_FRAMEWORK["PAGE_SIZE"] = 2
        response = auth_client.get(heart_rate_endpoints["list"])
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data["results"]) <= 2

    def test_list_heart_rates_unauthenticated(self, api_client, heart_rate_endpoints):
        response = api_client.get(heart_rate_endpoints["list"])
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # -----------------------------
    # CREATE HEART RATE
    # -----------------------------
    def test_create_heart_rate_success(self, auth_client, heart_rate_endpoints, heart_rate_payload):
        response = auth_client.post(heart_rate_endpoints["create"], heart_rate_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert HeartRate.objects.filter(patient_id=heart_rate_payload["patient"]).exists()

    def test_create_heart_rate_invalid_data(self, auth_client, heart_rate_endpoints):
        payload = {"bpm": -5}  # Invalid BPM
        response = auth_client.post(heart_rate_endpoints["create"], payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_heart_rate_unauthenticated(self, api_client, heart_rate_endpoints, heart_rate_payload):
        response = api_client.post(heart_rate_endpoints["create"], heart_rate_payload, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # -----------------------------
    # RETRIEVE HEART RATE
    # -----------------------------
    def test_retrieve_heart_rate_success(self, auth_client, heart_rate_endpoints, heart_rate_create):
        url = heart_rate_endpoints["detail"](heart_rate_create.id)
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["bpm"] == heart_rate_create.bpm

    def test_retrieve_heart_rate_not_found(self, auth_client, heart_rate_endpoints):
        url = heart_rate_endpoints   # Non-existent ID
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    # -----------------------------
    # UPDATE HEART RATE
    # -----------------------------
    def test_update_heart_rate_success(self, auth_client, heart_rate_endpoints, heart_rate_create):
        url = heart_rate_endpoints["detail"](heart_rate_create.id)
        payload = {
            "patient": heart_rate_create.patient.id,
            "bpm": 90,
            "recorded_at": heart_rate_create.recorded_at.isoformat()
        }
        response = auth_client.put(url, payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        heart_rate_create.refresh_from_db()
        assert heart_rate_create.bpm == 90

    def test_update_heart_rate_unauthenticated(self, api_client, heart_rate_endpoints, heart_rate_create):
        url = heart_rate_endpoints["detail"](heart_rate_create.id)
        payload = {"bpm": 100}
        response = api_client.put(url, payload, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # -----------------------------
    # DELETE HEART RATE
    # -----------------------------
    def test_delete_heart_rate_success(self, auth_client, heart_rate_endpoints, heart_rate_create):
        url = heart_rate_endpoints["detail"](heart_rate_create.id)
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not HeartRate.objects.filter(id=heart_rate_create.id).exists()

    def test_delete_heart_rate_unauthenticated(self, api_client, heart_rate_endpoints, heart_rate_create):
        url = heart_rate_endpoints["detail"](heart_rate_create.id)
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # -----------------------------
    # SEARCH & ORDERING
    # -----------------------------
    def test_search_heart_rate_by_patient_name(self, auth_client, heart_rate_endpoints, heart_rate_create):
        response = auth_client.get(f"{heart_rate_endpoints['list']}?search=John")
        assert response.status_code == status.HTTP_200_OK
        assert any(hr["patient_name"] == "John Doe" for hr in response.data["results"])

    def test_order_heart_rate_by_bpm(self, auth_client, heart_rate_endpoints, heart_rate_create):
        for bpm in [70, 65, 85]:
            HeartRate.objects.create(
                patient=heart_rate_create.patient,
                bpm=bpm,
                recorded_at=heart_rate_create.recorded_at,
                recorded_by=heart_rate_create.recorded_by
            )
        response = auth_client.get(f"{heart_rate_endpoints['list']}?ordering=bpm")
        bpm_list = [hr["bpm"] for hr in response.data["results"]]
        assert bpm_list == sorted(bpm_list)
