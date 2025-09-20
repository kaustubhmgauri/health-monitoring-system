"""
test_location.py
~~~~~~~~~~~~~~~~~~~~~~~~~
Tests for LocationViewSet covering full CRUD, pagination, and validation.
"""

import pytest
from rest_framework import status
from users.models import Location


@pytest.mark.django_db
class TestLocationEndpoints:

    # -----------------------------
    # LIST LOCATIONS
    # -----------------------------
    def test_list_locations_authenticated(self, auth_client, location_endpoints, settings):
        # Create sample locations
        for i in range(5):
            Location.objects.create(name=f"Location {i}", address_line=f"Address {i}")

        settings.REST_FRAMEWORK["PAGE_SIZE"] = 2

        response = auth_client.get(location_endpoints["list"])
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data["results"]) <= 2

    def test_list_locations_unauthenticated(self, api_client, location_endpoints):
        response = api_client.get(location_endpoints["list"])
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # -----------------------------
    # CREATE LOCATION
    # -----------------------------
    def test_create_location_success(self, auth_client, location_endpoints, location_payload):
        response = auth_client.post(location_endpoints["create"], location_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Location.objects.filter(name=location_payload["name"]).exists()

    def test_create_location_invalid_data(self, auth_client, location_endpoints):
        payload = {"name": "", "address": ""}
        response = auth_client.post(location_endpoints["create"], payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_location_unauthenticated(self, api_client, location_endpoints, location_payload):
        response = api_client.post(location_endpoints["create"], location_payload, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # -----------------------------
    # RETRIEVE LOCATION
    # -----------------------------
    def test_retrieve_location_success(self, auth_client, location_endpoints, location_payload):
        location = Location.objects.create(**location_payload)
        url = location_endpoints["detail"](location.id)
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == location_payload["name"]

    def test_retrieve_location_not_found(self, auth_client, location_endpoints):
        url = location_endpoints   # Non-existent ID
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    # -----------------------------
    # UPDATE LOCATION
    # -----------------------------
    def test_update_location_success(self, auth_client, location_endpoints, location_payload):
        location = Location.objects.create(**location_payload)
        url = location_endpoints["detail"](location.id)
        payload = {"name": "Updated Location", "address": "Updated Address"}
        response = auth_client.put(url, payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        location.refresh_from_db()
        assert location.name == "Updated Location"

    def test_update_location_unauthenticated(self, api_client, location_endpoints, location_payload):
        location = Location.objects.create(**location_payload)
        url = location_endpoints["detail"](location.id)
        payload = {"name": "Updated Location", "address": "Updated Address"}
        response = api_client.put(url, payload, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # -----------------------------
    # DELETE LOCATION
    # -----------------------------
    def test_delete_location_success(self, auth_client, location_endpoints, location_payload):
        location = Location.objects.create(**location_payload)
        url = location_endpoints["detail"](location.id)
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Location.objects.filter(id=location.id).exists()

    def test_delete_location_unauthenticated(self, api_client, location_endpoints, location_payload):
        location = Location.objects.create(**location_payload)
        url = location_endpoints["detail"](location.id)
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
