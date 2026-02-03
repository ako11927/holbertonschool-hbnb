"Users API for HBnB."
from flask_restx import Namespace, Resource, fields
from flask import request
from app import db
from app.models.user import User

api = Namespace("users", description="Users operations")

user_model = api.model(
    "User",
    {
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True),
        "is_admin": fields.Boolean(default=False)
    }
)

@api.route("/")
class UserList(Resource):
    @api.marshal_list_with(user_model, skip_none=True)
    def get(self):
        "Get all users"
        users = User.query.all()
        return [user.to_dict() for user in users], 200

    @api.expect(user_model, validate=True)
    def post(self):
        "Create a new user"
        data = api.payload
        if User.query.filter_by(email=data["email"]).first():
            return {"error": "Email already exists"}, 400

        user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            is_admin=data.get("is_admin", False)
        )
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

