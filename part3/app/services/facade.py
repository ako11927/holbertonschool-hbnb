from app.persistence.repository import InMemoryRepository, UserRepository
from app.models.user import User


class HBnBFacade:
    """Facade over persistence. User operations use UserRepository; rest use InMemoryRepository until migrated."""

    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User methods (all via UserRepository; no direct db.session)
    def create_user(self, user_data):
        """Create a new user. Hashes password before persisting (no plain password stored)."""
        password = user_data.get("password")
        if not password:
            raise ValueError("password required to create user")
        data = {k: v for k, v in user_data.items() if k != "password"}
        user = User(**data)
        user.hash_password(password)
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
        return self.user_repo.get_user_by_email(email)

    def update_user(self, user_id, user_data):
        """Update user information. Plain password in user_data is hashed before saving."""
        user = self.user_repo.get(user_id)
        if not user:
            return None
        if "email" in user_data and user_data["email"] != user.email:
            existing = self.get_user_by_email(user_data["email"])
            if existing and existing.id != user_id:
                raise ValueError("Email already registered")
        data = {k: v for k, v in user_data.items() if k != "password"}
        password = user_data.get("password")
        if password is not None:
            user.hash_password(password)
            data["password"] = user.password  # pass hashed value for repo.update
        self.user_repo.update(user_id, data)
        return self.user_repo.get(user_id)

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

    # Place methods
    def create_place(self, place_data):
        """Create a new place."""
        from app.models.place import Place
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Get place by ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Get all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update place information."""
        # First get the place
        place = self.place_repo.get(place_id)
        if not place:
            return None
        
        # Update the place
        place.update(place_data)
        return place
