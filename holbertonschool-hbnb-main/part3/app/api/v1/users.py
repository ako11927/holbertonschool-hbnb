"Users API for HBnB. All user operations go through the facade (no direct db.session)."
from flask_restx import Namespace, Resource, fields
from app.services import facade

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


@api.route("/")
class UserList(Resource):
    def get(self):
        "Get all users"
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200

    @api.expect(user_model, validate=True)
    def post(self):
        "Create a new user (password is hashed by facade)"
        data = api.payload
        if facade.get_user_by_email(data["email"]):
            return {"error": "Email already exists"}, 400
        try:
            user = facade.create_user(data)
            return user.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400


@api.route("/<string:user_id>")
class UserResource(Resource):
    def get(self, user_id):
        "Get user by ID"
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return user.to_dict(), 200
