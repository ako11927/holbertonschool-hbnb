import uuid
from typing import Dict, List, Optional
from datetime import datetime


class HBnBFacade:
    def __init__(self):
        self.users: Dict[str, 'User'] = {}
        self.places: Dict[str, 'Place'] = {}
        self.amenities: Dict[str, 'Amenity'] = {}
        self.reviews: Dict[str, 'Review'] = {}
        
        # Load sample data for testing
        self._load_sample_data()
    
    def _load_sample_data(self):
        """Load sample data for testing"""
        try:
            # Import models inside method to avoid circular imports
            from models import User, Amenity, Place, Review
            
            print("Loading sample data...")
            
            # Create sample users
            user1 = User(
                id=str(uuid.uuid4()),
                first_name="John",
                last_name="Doe",
                email="john.doe@example.com"
            )
            self.users[user1.id] = user1
            
            user2 = User(
                id=str(uuid.uuid4()),
                first_name="Jane",
                last_name="Smith",
                email="jane.smith@example.com"
            )
            self.users[user2.id] = user2
            
            # Create sample amenities
            wifi = Amenity(id=str(uuid.uuid4()), name="Wi-Fi")
            ac = Amenity(id=str(uuid.uuid4()), name="Air Conditioning")
            pool = Amenity(id=str(uuid.uuid4()), name="Pool")
            
            self.amenities[wifi.id] = wifi
            self.amenities[ac.id] = ac
            self.amenities[pool.id] = pool
            
            # Create sample place
            place1 = Place()
            place1.id = str(uuid.uuid4())
            place1.title = "Cozy Apartment"
            place1.description = "A nice place to stay"
            place1.price = 100.0
            place1.latitude = 37.7749
            place1.longitude = -122.4194
            place1.owner_id = user1.id
            place1.owner = user1
            place1.amenities = [wifi, ac]
            
            self.places[place1.id] = place1
            
            # Create sample review
            review1 = Review()
            review1.id = str(uuid.uuid4())
            review1.text = "Great place to stay!"
            review1.rating = 5
            review1.user_id = user2.id
            review1.place_id = place1.id
            review1.user = user2
            review1.place = place1
            
            self.reviews[review1.id] = review1
            place1.reviews.append(review1)
            
            print(f"Loaded {len(self.users)} users, {len(self.places)} places, "
                  f"{len(self.amenities)} amenities, {len(self.reviews)} reviews")
            
        except ImportError as e:
            print(f"Warning: Could not import models: {e}")
            print("Creating empty data structures...")
        except Exception as e:
            print(f"Error loading sample data: {e}")
    
    # ========== PLACE METHODS ==========
    
    def create_place(self, place_data: dict) -> 'Place':
        """Create a new place with validation"""
        try:
            from models import Place
            
            # Validate required fields
            required_fields = ['title', 'price', 'latitude', 'longitude', 'owner_id']
            for field in required_fields:
                if field not in place_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Validate owner exists
            owner_id = place_data.get('owner_id')
            if not owner_id or owner_id not in self.users:
                raise ValueError("Owner does not exist")
            
            # Create place
            place = Place()
            place.title = place_data.get('title', '')
            place.description = place_data.get('description', '')
            
            # Validate and set price
            price = place_data.get('price')
            try:
                place.price = float(price)
            except (ValueError, TypeError):
                raise ValueError("Price must be a valid number")
            
            # Validate and set latitude
            latitude = place_data.get('latitude')
            try:
                place.latitude = float(latitude)
            except (ValueError, TypeError):
                raise ValueError("Latitude must be a valid number")
            
            # Validate and set longitude
            longitude = place_data.get('longitude')
            try:
                place.longitude = float(longitude)
            except (ValueError, TypeError):
                raise ValueError("Longitude must be a valid number")
            
            place.owner_id = owner_id
            place.owner = self.users[owner_id]
            
            # Add amenities if provided
            amenity_ids = place_data.get('amenities', [])
            for amenity_id in amenity_ids:
                if amenity_id in self.amenities:
                    place.amenities.append(self.amenities[amenity_id])
            
            # Save place
            self.places[place.id] = place
            return place
            
        except ValueError as e:
            raise ValueError(f"Invalid place data: {str(e)}")
        except Exception as e:
            raise Exception(f"Error creating place: {str(e)}")
    
    def get_place(self, place_id: str) -> Optional['Place']:
        """Get place by ID with related entities"""
        place = self.places.get(place_id)
        if place and place.owner_id and not place.owner:
            place.owner = self.users.get(place.owner_id)
        return place
    
    def get_all_places(self) -> List['Place']:
        """Get all places"""
        return list(self.places.values())
    
    def update_place(self, place_id: str, place_data: dict) -> Optional['Place']:
        """Update a place"""
        place = self.places.get(place_id)
        if not place:
            return None
        
        try:
            # Update basic fields
            if 'title' in place_data:
                place.title = place_data['title']
            if 'description' in place_data:
                place.description = place_data['description']
            if 'price' in place_data:
                try:
                    place.price = float(place_data['price'])
                except (ValueError, TypeError):
                    raise ValueError("Price must be a valid number")
            if 'latitude' in place_data:
                try:
                    place.latitude = float(place_data['latitude'])
                except (ValueError, TypeError):
                    raise ValueError("Latitude must be a valid number")
            if 'longitude' in place_data:
                try:
                    place.longitude = float(place_data['longitude'])
                except (ValueError, TypeError):
                    raise ValueError("Longitude must be a valid number")
            
            # Update amenities if provided
            if 'amenities' in place_data:
                place.amenities = []
                for amenity_id in place_data['amenities']:
                    if amenity_id in self.amenities:
                        place.amenities.append(self.amenities[amenity_id])
            
            place.updated_at = datetime.now()
            return place
            
        except ValueError as e:
            raise ValueError(f"Invalid update data: {str(e)}")
    
    def get_reviews_by_place(self, place_id: str) -> List['Review']:
        """Get all reviews for a specific place"""
        return [review for review in self.reviews.values() 
                if review.place_id == place_id]
    
    # ========== REVIEW METHODS ==========
    
    def create_review(self, review_data: dict) -> 'Review':
        """Create a new review with validation"""
        try:
            from models import Review
            
            # Validate required fields
            required_fields = ['text', 'rating', 'user_id', 'place_id']
            for field in required_fields:
                if field not in review_data:
                    raise ValueError(f"Missing required field: {field}")
            
            text = review_data['text'].strip()
            rating = review_data['rating']
            user_id = review_data['user_id']
            place_id = review_data['place_id']
            
            # Validate text
            if not text:
                raise ValueError("Review text cannot be empty")
            
            # Validate rating
            try:
                rating = int(rating)
                if not 1 <= rating <= 5:
                    raise ValueError("Rating must be between 1 and 5")
            except (ValueError, TypeError):
                raise ValueError("Rating must be an integer between 1 and 5")
            
            # Validate user exists
            if user_id not in self.users:
                raise ValueError("User does not exist")
            
            # Validate place exists
            if place_id not in self.places:
                raise ValueError("Place does not exist")
            
            # Check if user already reviewed this place
            existing_review = next(
                (r for r in self.reviews.values() 
                 if r.user_id == user_id and r.place_id == place_id),
                None
            )
            if existing_review:
                raise ValueError("User has already reviewed this place")
            
            # Create review
            review = Review()
            review.text = text
            review.rating = rating
            review.user_id = user_id
            review.place_id = place_id
            review.user = self.users[user_id]
            review.place = self.places[place_id]
            
            # Save review
            self.reviews[review.id] = review
            
            # Add review to place
            place = self.places[place_id]
            place.reviews.append(review)
            
            return review
            
        except ValueError as e:
            raise ValueError(f"Invalid review data: {str(e)}")
        except Exception as e:
            raise Exception(f"Error creating review: {str(e)}")
    
    def get_review(self, review_id: str) -> Optional['Review']:
        """Get review by ID"""
        return self.reviews.get(review_id)
    
    def get_all_reviews(self) -> List['Review']:
        """Get all reviews"""
        return list(self.reviews.values())
    
    def update_review(self, review_id: str, review_data: dict) -> Optional['Review']:
        """Update a review"""
        review = self.reviews.get(review_id)
        if not review:
            return None
        
        try:
            if 'text' in review_data:
                text = review_data['text'].strip()
                if not text:
                    raise ValueError("Review text cannot be empty")
                review.text = text
            
            if 'rating' in review_data:
                try:
                    rating = int(review_data['rating'])
                    if not 1 <= rating <= 5:
                        raise ValueError("Rating must be between 1 and 5")
                    review.rating = rating
                except (ValueError, TypeError):
                    raise ValueError("Rating must be an integer between 1 and 5")
            
            review.updated_at = datetime.now()
            return review
            
        except ValueError as e:
            raise ValueError(f"Invalid update data: {str(e)}")
    
    def delete_review(self, review_id: str) -> bool:
        """Delete a review"""
        if review_id in self.reviews:
            review = self.reviews[review_id]
            
            # Remove review from place's reviews list
            if review.place_id in self.places:
                place = self.places[review.place_id]
                place.reviews = [r for r in place.reviews if r.id != review_id]
            
            del self.reviews[review_id]
            return True
        
        return False
    
    # ========== UTILITY METHODS ==========
    
    def get_user(self, user_id: str) -> Optional['User']:
        """Get user by ID"""
        return self.users.get(user_id)
    
    def get_amenity(self, amenity_id: str) -> Optional['Amenity']:
        """Get amenity by ID"""
        return self.amenities.get(amenity_id)


# Create global facade instance
facade = HBnBFacade()
