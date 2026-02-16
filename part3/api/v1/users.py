"""Users API: CRUD. POST and PUT restricted to admins; GET requires JWT."""
from flask import request, current_app
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

from .rbac import admin_required

api = Namespace("users", description="User operations")

user_model = api.model("User", {
    "id": fields.String(description="User ID"),
    "first_name": fields.String(description="First name"),
    "last_name": fields.String(description="Last name"),
    "email": fields.String(description="Email"),
    "is_admin": fields.Boolean(description="Admin flag"),
    "created_at": fields.DateTime(description="Created at"),
    "updated_at": fields.DateTime(description="Updated at"),
})

user_input_model = api.model("UserInput", {
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True),
    "email": fields.String(required=True),
    "password": fields.String(required=True),
    "is_admin": fields.Boolean(default=False),
})

user_update_model = api.model("UserUpdate", {
    "first_name": fields.String(),
    "last_name": fields.String(),
    "email": fields.String(),
    "password": fields.String(),
    "is_admin": fields.Boolean(),
})


@api.route("/")
class UserList(Resource):
    @jwt_required()
    @api.response(200, "List of users")
    def get(self):
        """List all users. Requires JWT."""
        from services import facade
        users = facade.get_all_users()
        return [u.to_dict() for u in users], 200

    @admin_required
    @api.expect(user_input_model, validate=True)
    @api.response(201, "User created", user_model)
    @api.response(400, "Invalid input or duplicate email")
    def post(self):
        """Create a new user. Admin only. Email must be unique; password hashed with Bcrypt."""
        data = request.get_json() or {}
        required = ["first_name", "last_name", "email", "password"]
        for k in required:
            if k not in data:
                return {"error": f"Missing required field: {k}"}, 400
        bcrypt = current_app.extensions.get("bcrypt")
        if not bcrypt:
            return {"error": "Password hashing not configured"}, 500
        pw_hash = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
        payload = {
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "email": data["email"],
            "password_hash": pw_hash,
            "is_admin": bool(data.get("is_admin", False)),
        }
        try:
            from services import facade
            user = facade.create_user(payload)
            return user.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400


@api.route("/<user_id>")
class UserResource(Resource):
    @jwt_required()
    @api.response(200, "User details", user_model)
    @api.response(404, "User not found")
    def get(self, user_id):
        """Get user by ID. Requires JWT."""
        from services import facade
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return user.to_dict(), 200

    @admin_required
    @api.expect(user_update_model)
    @api.response(200, "User updated")
    @api.response(400, "Invalid input or duplicate email")
    @api.response(404, "User not found")
    def put(self, user_id):
        """Update any user (including email and password). Admin only. Passwords hashed with Bcrypt."""
        data = request.get_json() or {}
        bcrypt = current_app.extensions.get("bcrypt")
        if not bcrypt:
            return {"error": "Password hashing not configured"}, 500
        upd = {k: v for k, v in data.items() if k in {"first_name", "last_name", "email", "password", "is_admin"}}
        if "password" in upd:
            upd["password_hash"] = bcrypt.generate_password_hash(upd.pop("password")).decode("utf-8")
        if not upd:
            from services import facade
            user = facade.get_user(user_id)
            if not user:
                return {"error": "User not found"}, 404
            return user.to_dict(), 200
        try:
            from services import facade
            user = facade.update_user(user_id, upd)
            if not user:
                return {"error": "User not found"}, 404
            return user.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 400
