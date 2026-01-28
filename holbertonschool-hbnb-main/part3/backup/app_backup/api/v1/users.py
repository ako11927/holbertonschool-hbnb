"""User routes namespace."""
from flask_restx import Namespace, Resource

# Create namespace
api = Namespace('users', description='User operations')

@api.route('/')
class UserList(Resource):
    """List all users or create new user."""
    def get(self):
        """Get all users."""
        return {'message': 'GET /users'}, 200
    
    def post(self):
        """Create a new user."""
        return {'message': 'POST /users'}, 201

@api.route('/<user_id>')
class UserDetail(Resource):
    """Get, update, or delete specific user."""
    def get(self, user_id):
        """Get user by ID."""
        return {'message': f'GET /users/{user_id}'}, 200
    
    def put(self, user_id):
        """Update user by ID."""
        return {'message': f'PUT /users/{user_id}'}, 200
    
    def delete(self, user_id):
        """Delete user by ID."""
        return {'message': f'DELETE /users/{user_id}'}, 204
