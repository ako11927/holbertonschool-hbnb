"""Auth namespace: login (email + password) -> JWT with id, email, is_admin.
   POST /auth/login: JSON {email, password} -> {access_token}. Token identity = user id; claims: email, is_admin."""
from flask import request, current_app
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token

api = Namespace("auth", description="Authentication")

login_model = api.model("Login", {
    "email": fields.String(required=True, description="User email"),
    "password": fields.String(required=True, description="User password"),
})

token_model = api.model("Token", {
    "access_token": fields.String(description="JWT access token"),
})


@api.route("/login")
class Login(Resource):
    @api.expect(login_model, validate=True)
    @api.response(200, "Login successful", token_model)
    @api.response(400, "Invalid input")
    @api.response(401, "Invalid email or password")
    def post(self):
        """Login with email and password. Returns JWT (identity=user id, claims: email, is_admin)."""
        data = request.get_json() or {}
        email = (data.get("email") or "").strip()
        password = data.get("password")
        if not email or password is None:
            return {"error": "email and password required"}, 400

        from services import facade
        user = facade.get_user_by_email(email)
        if not user:
            return {"error": "Invalid email or password"}, 401

        bcrypt = current_app.extensions.get("bcrypt")
        if not bcrypt or not getattr(user, "password_hash", None):
            return {"error": "Invalid email or password"}, 401
        if not bcrypt.check_password_hash(user.password_hash, password):
            return {"error": "Invalid email or password"}, 401

        token = create_access_token(
            identity=user.id,
            additional_claims={"email": user.email, "is_admin": getattr(user, "is_admin", False)},
        )
        return {"access_token": token}, 200
