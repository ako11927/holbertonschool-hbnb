from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

@api.route('/')
class UserList(Resource):
    @jwt_required()
    def post(self):
        """Create a new user (Admins only)"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload
        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        new_user.hash_password(user_data['password'])

        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201

    @jwt_required()
    def get(self):
        """List all users (Admins only)"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        users = facade.get_all_users()
        return [{'id': u.id, 'first_name': u.first_name, 'last_name': u.last_name, 'email': u.email} for u in users], 200

@api.route('/<string:user_id>')
class UserResource(Resource):
    @jwt_required()
    def get(self, user_id):
        """Get user by ID (Admins can get anyone, user can get self)"""
        claims = get_jwt()
        current_id = get_jwt_identity()
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        if not claims.get('is_admin', False) and user_id != current_id:
            return {'error': 'Unauthorized action'}, 403

        return {'id': user.id, 'first_name': user.first_name,
                'last_name': user.last_name, 'email': user.email}, 200

    @jwt_required()
    def put(self, user_id):
        """Update user (Admins can update anyone)"""
        claims = get_jwt()
        current_id = get_jwt_identity()
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        if not claims.get('is_admin', False) and user_id != current_id:
            return {'error': 'Unauthorized action'}, 403

        data = api.payload

        # Regular users cannot change email/password
        if not claims.get('is_admin', False):
            if 'email' in data or 'password' in data:
                return {'error': 'You cannot modify email or password'}, 400

        if 'email' in data:
            existing = facade.get_user_by_email(data['email'])
            if existing and existing.id != user_id:
                return {'error': 'Email already in use'}, 400

        updated_user = facade.update_user(user_id, data)
        if 'password' in data:
            updated_user.hash_password(data['password'])

        return {'id': updated_user.id, 'first_name': updated_user.first_name,
                'last_name': updated_user.last_name, 'email': updated_user.email}, 200
