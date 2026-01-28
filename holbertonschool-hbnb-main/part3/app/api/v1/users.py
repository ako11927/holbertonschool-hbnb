"Users API for HBnB."
from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models.user import User
from app.utils.auth_helpers import is_current_user_admin

api = Namespace("users", description="Users operations")

user_model = api.model(
    "User",
    {
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True),
        "is_admin": fields.Boolean(default=False),
    },
)

user_update_model = api.model(
    "UserUpdate",
    {
        "first_name": fields.String(required=False),
        "last_name": fields.String(required=False),
    },
)

user_admin_update_model = api.model(
    "UserAdminUpdate",
    {
        "first_name": fields.String(required=False),
        "last_name": fields.String(required=False),
        "email": fields.String(required=False),
        "password": fields.String(required=False),
    },
)


@api.route("/")
class UserList(Resource):
    @api.marshal_list_with(user_model, skip_none=True)
    def get(self):
        "Get all users (public)."
        users = User.query.all()
        return [user.to_dict() for user in users], 200

    @api.expect(user_model, validate=True)
    @api.response(201, "User created")
    @api.response(400, "Invalid input")
    @api.response(401, "Authentication required")
    @api.response(403, "Admin required")
    @jwt_required()
    def post(self):
        "Create a new user (admin only)."
        if not is_current_user_admin():
            return {"error": "Admin access required"}, 403
        data = api.payload
        if User.query.filter_by(email=data["email"]).first():
            return {"error": "Email already exists"}, 400

        user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            is_admin=data.get("is_admin", False),
        )
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201


@api.route("/<int:user_id>")
class UserDetail(Resource):
    @api.expect(user_admin_update_model)
    @api.response(200, "User updated")
    @api.response(403, "Forbidden")
    @api.response(404, "User not found")
    @api.response(400, "Invalid input")
    @jwt_required()
    def put(self, user_id):
        "Admin: update any user (including email/password). Non-admin: update own first_name/last_name only."
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        current_id = get_jwt_identity()
        try:
            current_id = int(current_id)
        except (ValueError, TypeError):
            return {"error": "Invalid token"}, 403

        data = api.payload or request.get_json() or {}
        is_admin = is_current_user_admin()

        if is_admin:
            if "first_name" in data:
                user.first_name = data["first_name"]
            if "last_name" in data:
                user.last_name = data["last_name"]
            if "email" in data:
                new_email = data["email"].strip()
                if new_email != user.email:
                    existing = User.query.filter_by(email=new_email).first()
                    if existing and existing.id != user_id:
                        return {"error": "Email already exists"}, 400
                    user.email = new_email
            if "password" in data and data["password"]:
                user.set_password(data["password"])
            db.session.commit()
            return user.to_dict(), 200

        if current_id != user_id:
            return {"error": "You can only update your own profile"}, 403
        if "email" in data or "password" in data:
            return {"error": "Email and password cannot be changed"}, 400
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]
        db.session.commit()
        return user.to_dict(), 200

