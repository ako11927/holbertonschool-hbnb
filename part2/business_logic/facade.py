"""Facade pattern implementation for business logic."""
from typing import Dict, Any, Optional, List
from persistence.in_memory_repository import InMemoryRepository
from .models.user import User
from .models.place import Place
from .models.review import Review
from .models.amenity import Amenity
from .models.city import City
from .models.state import State
from .exceptions import ValidationError, NotFoundError, DuplicateError


class HBnBFacade:
    """
    Facade for HBnB business logic.
    
    This class provides a simplified interface to the complex business logic
    and manages relationships between entities.
    """
    
    def __init__(self):
        """Initialize facade with repositories."""
        self.user_repository = InMemoryRepository()
        self.place_repository = InMemoryRepository()
        self.review_repository = InMemoryRepository()
        self.amenity_repository = InMemoryRepository()
        self.city_repository = InMemoryRepository()
        self.state_repository = InMemoryRepository()
        
        # Initialize relationship caches
        self._user_reviews: Dict[str, List[str]] = {}  # user_id -> [review_ids]
        self._place_reviews: Dict[str, List[str]] = {}  # place_id -> [review_ids]
        self._place_amenities: Dict[str, List[str]] = {}  # place_id -> [amenity_ids]
        self._state_cities: Dict[str, List[str]] = {}  # state_id -> [city_ids]
    
    # User Operations
    def create_user(self, user_data: Dict[str, Any]) -> User:
        """Create a new user."""
        # Check for duplicate email
        users = self.user_repository.get_all()
        for user in users:
            if hasattr(user, 'email') and user.email == user_data.get('email'):
                raise DuplicateError("User with this email already exists")
        
        user = User(**user_data)
        self.user_repository.create(user)
        self._user_reviews[user.id] = []
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get a user by ID."""
        user = self.user_repository.get(user_id)
        if user:
            # Populate user's reviews
            review_ids = self._user_reviews.get(user_id, [])
            user.reviews = [self.review_repository.get(rid) for rid in review_ids]
            # Populate user's places
            user.places = [p for p in self.place_repository.get_all() 
                          if hasattr(p, 'user_id') and p.user_id == user_id]
        return user
    
    # Place Operations
    def create_place(self, place_data: Dict[str, Any]) -> Place:
        """Create a new place."""
        # Verify user exists
        user = self.user_repository.get(place_data.get('user_id', ''))
        if not user:
            raise ValidationError("User does not exist")
        
        # Verify city exists
        city = self.city_repository.get(place_data.get('city_id', ''))
        if not city:
            raise ValidationError("City does not exist")
        
        place = Place(**place_data)
        self.place_repository.create(place)
        self._place_reviews[place.id] = []
        self._place_amenities[place.id] = []
        return place
    
    def get_place(self, place_id: str) -> Optional[Place]:
        """Get a place by ID."""
        place = self.place_repository.get(place_id)
        if place:
            # Populate place's reviews
            review_ids = self._place_reviews.get(place_id, [])
            place.reviews = [self.review_repository.get(rid) for rid in review_ids]
            # Populate place's amenities
            amenity_ids = self._place_amenities.get(place_id, [])
            place.amenities = [self.amenity_repository.get(aid) for aid in amenity_ids]
        return place
    
    # Review Operations
    def create_review(self, review_data: Dict[str, Any]) -> Review:
        """Create a new review."""
        # Verify user exists
        user = self.user_repository.get(review_data.get('user_id', ''))
        if not user:
            raise ValidationError("User does not exist")
        
        # Verify place exists
        place = self.place_repository.get(review_data.get('place_id', ''))
        if not place:
            raise ValidationError("Place does not exist")
        
        # Check if user already reviewed this place
        review_ids = self._user_reviews.get(user.id, [])
        for rid in review_ids:
            review = self.review_repository.get(rid)
            if review and review.place_id == place.id:
                raise DuplicateError("User has already reviewed this place")
        
        review = Review(**review_data)
        self.review_repository.create(review)
        
        # Update relationship caches
        self._user_reviews.setdefault(user.id, []).append(review.id)
        self._place_reviews.setdefault(place.id, []).append(review.id)
        
        return review
    
    # Amenity Operations
    def create_amenity(self, amenity_data: Dict[str, Any]) -> Amenity:
        """Create a new amenity."""
        amenity = Amenity(**amenity_data)
        self.amenity_repository.create(amenity)
        return amenity
    
    def add_amenity_to_place(self, place_id: str, amenity_id: str) -> bool:
        """Add amenity to place."""
        place = self.place_repository.get(place_id)
        amenity = self.amenity_repository.get(amenity_id)
        
        if not place:
            raise NotFoundError("Place not found")
        if not amenity:
            raise NotFoundError("Amenity not found")
        
        if amenity_id not in self._place_amenities.get(place_id, []):
            self._place_amenities.setdefault(place_id, []).append(amenity_id)
            place.amenity_ids.append(amenity_id)
            place.amenities.append(amenity)
            return True
        
        return False
    
    # City and State Operations
    def create_state(self, state_data: Dict[str, Any]) -> State:
        """Create a new state."""
        state = State(**state_data)
        self.state_repository.create(state)
        self._state_cities[state.id] = []
        return state
    
    def create_city(self, city_data: Dict[str, Any]) -> City:
        """Create a new city."""
        # Verify state exists
        state = self.state_repository.get(city_data.get('state_id', ''))
        if not state:
            raise ValidationError("State does not exist")
        
        city = City(**city_data)
        self.city_repository.create(city)
        
        # Update relationship cache
        self._state_cities.setdefault(state.id, []).append(city.id)
        
        return city
    
    # Bulk get operations
    def get_all_users(self) -> List[User]:
        """Get all users."""
        return self.user_repository.get_all()
    
    def get_all_places(self) -> List[Place]:
        """Get all places."""
        return self.place_repository.get_all()
    
    def get_all_reviews(self) -> List[Review]:
        """Get all reviews."""
        return self.review_repository.get_all()
    
    def get_all_amenities(self) -> List[Amenity]:
        """Get all amenities."""
        return self.amenity_repository.get_all()
