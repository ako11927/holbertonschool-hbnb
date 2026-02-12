"""Facade pattern for business logic operations with relationships."""
from app.repositories.user_repository import UserRepository
from app.repositories.place_repository import PlaceRepository
from app.repositories.review_repository import ReviewRepository
from app.repositories.amenity_repository import AmenityRepository


class HBnBFacade:
    """Facade for HBnB business operations with relationships."""
    
    def __init__(self):
        """Initialize facade with repositories."""
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()
    
    # User operations with relationships
    def create_user(self, user_data):
        """Create a new user."""
        user = self.user_repo.create_user(user_data)
        if not user:
            raise ValueError("User with this email already exists")
        return user
    
    def get_user(self, user_id):
        """Get a user by ID."""
        return self.user_repo.get(user_id)
    
    def get_user_with_relationships(self, user_id):
        """Get a user with all relationships."""
        return self.user_repo.get_user_with_relationships(user_id)
    
    def get_user_places(self, user_id):
        """Get all places owned by a user."""
        return self.user_repo.get_user_places(user_id)
    
    def get_user_reviews(self, user_id):
        """Get all reviews written by a user."""
        return self.user_repo.get_user_reviews(user_id)
    
    # Place operations with relationships
    def create_place(self, place_data):
        """Create a new place with owner relationship."""
        place = self.place_repo.create_place(place_data)
        return place
    
    def get_place(self, place_id):
        """Get a place by ID."""
        return self.place_repo.get(place_id)
    
    def get_place_with_relationships(self, place_id):
        """Get a place with all relationships."""
        return self.place_repo.get_place_with_relationships(place_id)
    
    def get_places_by_owner(self, owner_id):
        """Get all places owned by a user."""
        return self.place_repo.get_places_by_owner(owner_id)
    
    def get_place_reviews(self, place_id):
        """Get all reviews for a place."""
        return self.place_repo.get_place_reviews(place_id)
    
    def add_amenity_to_place(self, place_id, amenity_id):
        """Add an amenity to a place."""
        return self.place_repo.add_amenity_to_place(place_id, amenity_id)
    
    def remove_amenity_from_place(self, place_id, amenity_id):
        """Remove an amenity from a place."""
        return self.place_repo.remove_amenity_from_place(place_id, amenity_id)
    
    # Review operations with relationships
    def create_review(self, review_data):
        """Create a new review with user and place relationships."""
        return self.review_repo.create_review(review_data)
    
    def get_review(self, review_id):
        """Get a review by ID."""
        return self.review_repo.get(review_id)
    
    def get_review_with_relationships(self, review_id):
        """Get a review with all relationships."""
        return self.review_repo.get_review_with_relationships(review_id)
    
    def get_reviews_by_user(self, user_id):
        """Get all reviews by a user."""
        return self.review_repo.get_reviews_by_user(user_id)
    
    def get_reviews_by_place(self, place_id):
        """Get all reviews for a place."""
        return self.review_repo.get_reviews_by_place(place_id)
    
    # Amenity operations
    def create_amenity(self, amenity_data):
        """Create a new amenity."""
        try:
            amenity = self.amenity_repo.create_amenity(amenity_data)
            return amenity
        except ValueError as e:
            raise e
