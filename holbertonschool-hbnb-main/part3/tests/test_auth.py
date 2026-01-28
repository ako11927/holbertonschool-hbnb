"""Authentication and registration tests for the HBnB API."""

import pytest


@pytest.mark.usefixtures("client", "db")
def test_user_registration_requires_admin_and_creates_user(client, admin_token):
    """POST /api/v1/users should allow an admin to register a new user."""
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "password123",
        "is_admin": False,
    }
    headers = {"Authorization": f"Bearer {admin_token}"}

    response = client.post("/api/v1/users", json=payload, headers=headers)

    assert response.status_code == 201
    data = response.get_json() or {}
    assert data["email"] == payload["email"]
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    # Password hash must never be returned by the API.
    assert "password" not in data


@pytest.mark.usefixtures("client", "db")
def test_user_login_returns_access_token(client, admin_user):
    """POST /api/v1/auth/login should authenticate and return an access token."""
    # The admin_user fixture has already created a user with a known password.
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "adminpass"},
    )

    assert response.status_code == 200
    data = response.get_json() or {}
    # Ensure a token is present and looks like a non-empty string.
    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert data["access_token"]

