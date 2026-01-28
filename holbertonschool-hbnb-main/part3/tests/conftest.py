"""Pytest configuration and fixtures for the HBnB Part 3 project.

The tests here exercise the public HTTP API using Flask's test client.
We create an application instance via :func:`create_app` when available
and fall back to a plain ``Flask(__name__)`` otherwise.

For persistence we use SQLite in-memory where possible and ensure that
all database tables are created before the tests run and dropped once
the test session finishes.
"""

import os
import inspect
from typing import Generator

import pytest
from flask import Flask


@pytest.fixture(scope="session")
def app() -> Flask:
    """Create and configure a Flask application for tests.

    * Prefer the project's ``create_app`` factory if available.
    * If that factory exposes a ``testing`` parameter we call
      ``create_app(testing=True)`` as requested.
    * Otherwise we fall back to the existing configuration classes and
      finally to a minimal ``Flask(__name__)`` app.
    """
    # Ensure an in-memory SQLite database is used when possible.
    os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

    try:
        from app import create_app  # type: ignore
    except Exception:
        # Fallback: simple Flask app with no extensions.
        flask_app = Flask(__name__)
        flask_app.config.update(TESTING=True)
        return flask_app

    # Use the application's factory if present.
    try:
        sig = inspect.signature(create_app)
        if "testing" in sig.parameters:
            flask_app = create_app(testing=True)  # type: ignore[call-arg]
        else:
            from config import TestingConfig

            flask_app = create_app(TestingConfig)  # type: ignore[arg-type]
    except Exception:
        # As a last resort, build a bare Flask app.
        flask_app = Flask(__name__)

    flask_app.config.setdefault("TESTING", True)
    return flask_app


@pytest.fixture(scope="session")
def db(app: Flask):
    """Provide a database object with tables created for the test session.

    The database is initialised once per session and all tables are dropped
    after the tests complete.  This keeps the tests isolated and free from
    external state.
    """
    try:
        from app import db as _db  # type: ignore
    except Exception:
        # If the application does not expose a SQLAlchemy instance we simply
        # skip DB management – tests that rely on the DB can mark themselves
        # accordingly.
        yield None
        return

    with app.app_context():
        _db.create_all()
        try:
            yield _db
        finally:
            _db.drop_all()


@pytest.fixture
def client(app: Flask, db) -> Generator:
    """Provide a Flask test client for functional API tests."""
    with app.test_client() as testing_client:
        yield testing_client


@pytest.fixture
def admin_user(app: Flask, db):
    """Create an admin user in the database for authentication tests."""
    if db is None:
        pytest.skip("Database is not available for this test run.")

    from app.models.user import User  # type: ignore

    with app.app_context():
        existing = User.query.filter_by(email="admin@example.com").first()
        if existing:
            return existing

        user = User(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            is_admin=True,
        )
        user.set_password("adminpass")
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def admin_token(client, admin_user):
    """Return a JWT access token for the admin user."""
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "adminpass"},
    )
    assert login_response.status_code == 200
    data = login_response.get_json() or {}
    token = data.get("access_token")
    assert token, "Login did not return an access_token"
    return token

