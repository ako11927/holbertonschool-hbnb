"""Auth helpers for RBAC: get current user and admin check."""
from flask_jwt_extended import get_jwt_identity


def get_current_user():
    """Return the User for the JWT identity, or None."""
    from app.models.user import User
    uid = get_jwt_identity()
    if uid is None:
        return None
    try:
        return User.query.get(int(uid))
    except (ValueError, TypeError):
        return None


def is_current_user_admin():
    """Return True if the current JWT identity is an admin user."""
    user = get_current_user()
    return user is not None and getattr(user, 'is_admin', False)
