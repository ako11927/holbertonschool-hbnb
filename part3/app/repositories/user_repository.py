"""User repository for database operations with relationships."""
from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    """Repository for User model operations with relationships."""
    
    def __init__(self):
        """Initialize UserRepository with User model."""
        super().__init__(User)
    
    def get_user_by_email(self, email):
        """Get a user by email."""
        return self.model.query.filter_by(email=email).first()
    
    def authenticate_user(self, email, password):
        """Authenticate a user by email and password."""
        user = self.get_user_by_email(email)
        if user and user.verify_password(password):
            return user
        return None
    
    def create_user(self, user_data):
        """Create a new user with password hashing."""
        # Check if email already exists
        existing_user = self.get_user_by_email(user_data.get('email'))
        if existing_user:
            return None
        
        # Create user instance
        user = User(
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            is_admin=user_data.get('is_admin', False)
        )
        
        # Hash password
        user.hash_password(user_data['password'])
        
        # Save to database
        return self.add(user)
    
    def update_user(self, user_id, user_data):
        """Update a user with proper password handling."""
        user = self.get(user_id)
        if not user:
            return None
        
        # Handle password update
        if 'password' in user_data:
            user.hash_password(user_data.pop('password'))
        
        # Handle email uniqueness
        if 'email' in user_data and user_data['email'] != user.email:
            existing_user = self.get_user_by_email(user_data['email'])
            if existing_user:
                raise ValueError("Email already exists")
        
        # Update other fields
        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        db.session.commit()
        return user
    
    def get_user_with_relationships(self, user_id):
        """Get a user with all relationships loaded."""
        from sqlalchemy.orm import joinedload
        user = self.model.query.options(
            joinedload(User.places),
            joinedload(User.reviews)
        ).get(user_id)
        return user
    
    def get_user_places(self, user_id):
        """Get all places owned by a user."""
        user = self.get(user_id)
        if user:
            return user.places
        return []
    
    def get_user_reviews(self, user_id):
        """Get all reviews written by a user."""
        user = self.get(user_id)
        if user:
            return user.reviews
        return []
