"""RBAC helpers: admin-only checks using JWT claims (is_admin)."""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, jwt_required


def admin_required(fn):
    """Decorator: require JWT and is_admin in claims. Return 403 if not admin."""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        is_admin = claims.get("is_admin")
        if is_admin is not True:
            return jsonify({"error": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper
