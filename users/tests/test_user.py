"""
test_user.py
~~~~~~~~~~~~~~~~~~~~~
Tests for UserViewSet.
"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestUserEndpoints:

    # -----------------------------
    # REGISTER
    # -----------------------------
    def test_register_success(self, api_client, register_payload, user_endpoints):
        response = api_client.post(user_endpoints["register"], register_payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert "message" in response.data
        assert User.objects.filter(username=register_payload["username"]).exists()

    def test_register_invalid_data(self, api_client, user_endpoints):
        payload = {"username": "", "password": ""}
        response = api_client.post(user_endpoints["register"], payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    # -----------------------------
    # LOGIN
    # -----------------------------
    def test_login_success(self, api_client, login_payload, user_endpoints, test_user):
        response = api_client.post(user_endpoints["login"], login_payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data
        assert response.data["user"]["username"] == login_payload["username"]

    def test_login_invalid_credentials(self, api_client, user_endpoints):
        payload = {"username": "wronguser", "password": "wrongpass"}
        response = api_client.post(user_endpoints["login"], payload, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_missing_fields(self, api_client, user_endpoints):
        payload = {"username": "testuser"}
        response = api_client.post(user_endpoints["login"], payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    # -----------------------------
    # LIST USERS
    # -----------------------------
    def test_list_users_admin_success(self, admin_auth_client, user_endpoints):
        response = admin_auth_client.get(user_endpoints["list_users"])
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_list_users_non_admin_forbidden(self, auth_client, user_endpoints):
        response = auth_client.get(user_endpoints["list_users"])
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_users_unauthenticated(self, api_client, user_endpoints):
        response = api_client.get(user_endpoints["list_users"])
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
