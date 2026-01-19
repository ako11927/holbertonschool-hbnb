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
