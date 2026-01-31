#!/bin/bash
echo "=== Fixing Task 02 Implementation ==="

# 1. Fix User Model
echo "1. Fixing User Model..."
cat > app/models/user.py << 'USEREOF'
"""User model for HBnB."""
import uuid
from datetime import datetime

class User:
    """User class representing a user in the system."""
    
    def __init__(self, **kwargs):
        """Initialize a new User instance."""
        self.id = str(uuid.uuid4())
        self.first_name = kwargs.get('first_name', '')
        self.last_name = kwargs.get('last_name', '')
        self.email = kwargs.get('email', '')
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        # Set additional attributes if provided
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def update(self, data):
        """Update user attributes."""
        updatable_fields = ['first_name', 'last_name', 'email']
        for field in updatable_fields:
            if field in data:
                setattr(self, field, data[field])
        self.updated_at = datetime.now()
    
    def to_dict(self):
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f"<User {self.id}: {self.first_name} {self.last_name}>"
USEREOF

# 2. Fix Facade
echo "2. Fixing Facade..."
cat > app/services/facade.py << 'FACADEEOF'
from app.persistence.repository import InMemoryRepository
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User methods
    def create_user(self, user_data):
        """Create a new user."""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Get user by ID."""
        return self.user_repo.get(user_id)

    def get_all_users(self):
        """Get all users."""
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        """Get user by email."""
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        """Update user information."""
        # First get the user
        user = self.user_repo.get(user_id)
        if not user:
            return None
        
        # Check if email is being changed and if it's unique
        if 'email' in user_data and user_data['email'] != user.email:
            existing = self.get_user_by_email(user_data['email'])
            if existing and existing.id != user_id:
                raise ValueError("Email already registered")
        
        # Update the user
        user.update(user_data)
        return user
FACADEEOF

# 3. Fix Users API
echo "3. Fixing Users API..."
cat > app/api/v1/users.py << 'USERAPIEOF'
"""User API endpoints."""
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Check email uniqueness
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Get list of all users"""
        users = facade.get_all_users()
        return [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
            for user in users
        ], 200

@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Email already registered or invalid data')
    def put(self, user_id):
        """Update user information"""
        user_data = api.payload
        
        try:
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                return {'error': 'User not found'}, 404
            
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
USERAPIEOF

# 4. Fix routes.py
echo "4. Fixing routes.py..."
cat > app/api/v1/routes.py << 'ROUTESEOF'
"""API v1 routes configuration."""
from flask_restx import Resource

# Status endpoint (minimal - namespaces are registered in app/__init__.py)
from flask import Blueprint
from flask_restx import Api

# Create a blueprint for API v1
blueprint = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# Create main API instance attached to the blueprint
api = Api(
    blueprint,
    version='1.0',
    title='HBnB API',
    description='HBnB API operations',
    doc='/docs'
)

# Status endpoint
@api.route('/status')
class Status(Resource):
    """API status endpoint."""
    def get(self):
        return {'status': 'OK', 'version': '1.0'}
ROUTESEOF

# 5. Fix app/__init__.py
echo "5. Fixing app/__init__.py..."
cat > app/__init__.py << 'INITEOF'
from flask import Flask
from flask_restx import Api

def create_app():
    app = Flask(__name__)
    
    # Create API instance
    api = Api(app,
              version='1.0',
              title='HBnB API',
              description='HBnB Application API',
              doc='/api/v1/')
    
    # Import and register namespaces directly (as shown in Task 02)
    try:
        from .api.v1.users import api as users_ns
        from .api.v1.places import api as places_ns
        from .api.v1.reviews import api as reviews_ns
        from .api.v1.amenities import api as amenities_ns
        
        api.add_namespace(users_ns, path='/api/v1/users')
        api.add_namespace(places_ns, path='/api/v1/places')
        api.add_namespace(reviews_ns, path='/api/v1/reviews')
        api.add_namespace(amenities_ns, path='/api/v1/amenities')
        
        print("✅ All API namespaces registered")
    except ImportError as e:
        print(f"⚠️ Could not import all namespaces: {e}")
    
    return app
INITEOF

echo "=== Fix Complete ==="
echo "Run: python3 quick_test.py"
