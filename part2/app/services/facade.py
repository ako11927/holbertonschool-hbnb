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

    # Amenity methods
    def create_amenity(self, amenity_data):
        """Create a new amenity."""
        from app.models.amenity import Amenity
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Get amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Get all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update amenity information."""
        # First get the amenity
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        
        # Update the amenity
        amenity.update(amenity_data)
        return amenity
