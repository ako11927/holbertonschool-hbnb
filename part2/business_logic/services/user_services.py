"""User service for business logic operations."""
from business_logic.facade import HBnBFacade
from business_logic.models.user import User

class UserService:
    """Service for user operations."""
    
    def __init__(self, facade=None):
        """Initialize user service."""
        self.facade = facade or HBnBFacade()
    
    def register_user(self, user_data):
        """Register a new user."""
        # Validate required fields
        required_fields = ['email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if field not in user_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Create and return user
        return self.facade.create_user(user_data)
    
    def get_user_profile(self, user_id):
        """Get user profile by ID."""
        user = self.facade.get_user(user_id)
        if not user:
            raise ValueError(f"User not found: {user_id}")
        return user.to_dict()
    
    def update_user_profile(self, user_id, update_data):
        """Update user profile."""
        # Remove fields that shouldn't be updated
        protected_fields = ['id', 'created_at']
        for field in protected_fields:
            update_data.pop(field, None)
        
        return self.facade.update_user(user_id, update_data)
