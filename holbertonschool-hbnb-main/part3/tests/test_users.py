"""User endpoint authorisation tests."""

import pytest


@pytest.mark.usefixtures("client", "db")
def test_get_users_requires_jwt_token(client):
    """GET /api/v1/users without a JWT should not be allowed.

    Depending on how Flask-JWT-Extended is configured, this may result in
    401 (unauthorised) or 422 (missing/invalid token).  In all cases the
    endpoint must not succeed with a 2xx response.
    """
    response = client.get("/api/v1/users")
    assert response.status_code not in (200, 201, 204)


@pytest.mark.usefixtures("client", "db")
def test_get_users_with_valid_token_returns_200(client, admin_token, admin_user):
    """GET /api/v1/users with a valid JWT should succeed with status 200."""
    headers = {"Authorization": f"Bearer {admin_token}"}

    response = client.get("/api/v1/users", headers=headers)

    assert response.status_code == 200
    data = response.get_json() or []
    assert isinstance(data, list)
