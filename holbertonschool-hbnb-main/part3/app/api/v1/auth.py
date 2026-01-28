"""Auth API: login and JWT issuance."""
from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import create_access_token

from app.models.user import User


api = Namespace("auth", description="Authentication")

login_model = api.model(
    "Login",
    {
        "email": fields.String(required=True),
        "password": fields.String(required=True),
    },
)


@api.route("/login")
class Login(Resource):
    @api.expect(login_model, validate=True)
    def post(self):
        """Authenticate and return JWT access token."""
        data = api.payload or request.get_json() or {}
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return {"error": "Email and password are required"}, 400
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return {"error": "Invalid email or password"}, 401
        identity = str(user.id)
        token = create_access_token(identity=identity)
        return {"access_token": token}, 200
