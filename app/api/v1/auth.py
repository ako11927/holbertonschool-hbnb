from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload

        # Step 1: Retrieve user by email
        user = facade.get_user_by_email(credentials['email'])

        # Step 2: Check credentials
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Step 3: Create JWT token
        access_token = create_access_token(
            identity=str(user.id),  # user ID as identity
            additional_claims={"is_admin": user.is_admin}  # extra claim
        )

        # Step 4: Return token
        return {'access_token': access_token}, 200
