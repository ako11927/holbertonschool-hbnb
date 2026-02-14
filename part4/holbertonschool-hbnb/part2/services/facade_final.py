import uuid
from typing import Dict, List, Optional
from datetime import datetime

# Use string type hints to avoid import issues at module level
class HBnBFacadeFinal:
    def __init__(self):
        self.users: Dict[str, 'User'] = {}
        self.places: Dict[str, 'Place'] = {}
        self.amenities: Dict[str, 'Amenity'] = {}
        self.reviews: Dict[str, 'Review'] = {}
        
        # Load sample data
        self._load_sample_data()
    
    def _load_sample_data(self):
        """Load sample data"""
        try:
            # Import models
            from models.user import User
            from models.amenity import Amenity
            from models.place import Place
            from models.review import Review
            
            print("Loading sample data for testing...")
            
            # Create users
            user1 = User(id=str(uuid.uuid4()), first_name="John", last_name="Doe", email="john@example.com")
            user2 = User(id=str(uuid.uuid4()), first_name="Jane", last_name="Smith", email="jane@example.com")
            
            self.users[user1.id] = user1
            self.users[user2.id] = user2
            
            # Create amenities
            wifi = Amenity(id=str(uuid.uuid4()), name="Wi-Fi")
            ac = Amenity(id=str(uuid.uuid4()), name="Air Conditioning")
            pool = Amenity(id=str(uuid.uuid4()), name="Pool")
            
            self.amenities[wifi.id] = wifi
            self.amenities[ac.id] = ac
            self.amenities[pool.id] = pool
            
            # Create a place - careful with initialization
            place = Place()
            # Set ID first
            place.id = str(uuid.uuid4())
            # Set basic attributes
            place.title = "Cozy Apartment"
            place.description = "A nice place to stay"
            
            # Set numeric attributes directly to avoid property issues
            place._price = 100.0  # Set private attribute directly
            place._latitude = 37.7749
            place._longitude = -122.4194
            
            place.owner_id = user1.id
            place.owner = user1
            place.amenities = [wifi, ac]
            
            self.places[place.id] = place
            
            # Create a review
            review = Review()
            review.id = str(uuid.uuid4())
            review.text = "Great place! Very comfortable."
            review.rating = 5
            review.user_id = user2.id
            review.place_id = place.id
            review.user = user2
            review.place = place
            
            self.reviews[review.id] = review
            place.reviews.append(review)
            
            print(f"✓ Loaded: {len(self.users)} users, {len(self.places)} places, "
                  f"{len(self.amenities)} amenities, {len(self.reviews)} reviews")
            
        except Exception as e:
            print(f"⚠ Could not load sample data: {e}")
            # Continue with empty data
    
    def create_place(self, data: dict) -> 'Place':
        """Create a new place"""
        try:
            from models.place import Place
            
            # Check required fields
            required = ['title', 'price', 'latitude', 'longitude', 'owner_id']
            for field in required:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Check owner exists
            owner_id = data['owner_id']
            if owner_id not in self.users:
                raise ValueError(f"Owner {owner_id} not found")
            
            # Create place
            place = Place()
            place.id = str(uuid.uuid4())
            place.title = data['title']
            place.description = data.get('description', '')
            
            # Set numeric values
            try:
                place.price = float(data['price'])
            except (ValueError, TypeError):
                raise ValueError("Price must be a number")
            
            try:
                place.latitude = float(data['latitude'])
            except (ValueError, TypeError):
                raise ValueError("Latitude must be a number")
            
            try:
                place.longitude = float(data['longitude'])
            except (ValueError, TypeError):
                raise ValueError("Longitude must be a number")
            
            place.owner_id = owner_id
            place.owner = self.users[owner_id]
            
            # Add amenities
            for amenity_id in data.get('amenities', []):
                if amenity_id in self.amenities:
                    place.amenities.append(self.amenities[amenity_id])
            
            # Save
            self.places[place.id] = place
            return place
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Failed to create place: {e}")
    
    def get_place(self, place_id: str) -> Optional['Place']:
        """Get place by ID"""
        return self.places.get(place_id)
    
    def get_all_places(self) -> List['Place']:
        """Get all places"""
        return list(self.places.values())
    
    def update_place(self, place_id: str, data: dict) -> Optional['Place']:
        """Update a place"""
        place = self.places.get(place_id)
        if not place:
            return None
        
        # Update fields
        if 'title' in data:
            place.title = data['title']
        if 'description' in data:
            place.description = data['description']
        if 'price' in data:
            try:
                place.price = float(data['price'])
            except (ValueError, TypeError):
                pass
        if 'latitude' in data:
            try:
                place.latitude = float(data['latitude'])
            except (ValueError, TypeError):
                pass
        if 'longitude' in data:
            try:
                place.longitude = float(data['longitude'])
            except (ValueError, TypeError):
                pass
        
        place.updated_at = datetime.now()
        return place
    
    def get_reviews_by_place(self, place_id: str) -> List['Review']:
        """Get reviews for a place"""
        return [r for r in self.reviews.values() if r.place_id == place_id]
    
    def create_review(self, data: dict) -> 'Review':
        """Create a new review"""
        try:
            from models.review import Review
            
            # Check required fields
            required = ['text', 'rating', 'user_id', 'place_id']
            for field in required:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")
            
            text = data['text'].strip()
            if not text:
                raise ValueError("Review text cannot be empty")
            
            try:
                rating = int(data['rating'])
                if not 1 <= rating <= 5:
                    raise ValueError("Rating must be between 1 and 5")
            except (ValueError, TypeError):
                raise ValueError("Rating must be an integer")
            
            user_id = data['user_id']
            place_id = data['place_id']
            
            if user_id not in self.users:
                raise ValueError(f"User {user_id} not found")
            if place_id not in self.places:
                raise ValueError(f"Place {place_id} not found")
            
            # Create review
            review = Review()
            review.id = str(uuid.uuid4())
            review.text = text
            review.rating = rating
            review.user_id = user_id
            review.place_id = place_id
            review.user = self.users[user_id]
            review.place = self.places[place_id]
            
            # Save
            self.reviews[review.id] = review
            self.places[place_id].reviews.append(review)
            
            return review
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Failed to create review: {e}")
    
    def get_review(self, review_id: str) -> Optional['Review']:
        """Get review by ID"""
        return self.reviews.get(review_id)
    
    def get_all_reviews(self) -> List['Review']:
        """Get all reviews"""
        return list(self.reviews.values())
    
    def update_review(self, review_id: str, data: dict) -> Optional['Review']:
        """Update a review"""
        review = self.reviews.get(review_id)
        if not review:
            return None
        
        if 'text' in data:
            text = data['text'].strip()
            if text:
                review.text = text
        
        if 'rating' in data:
            try:
                rating = int(data['rating'])
                if 1 <= rating <= 5:
                    review.rating = rating
            except (ValueError, TypeError):
                pass
        
        review.updated_at = datetime.now()
        return review
    
    def delete_review(self, review_id: str) -> bool:
        """Delete a review"""
        if review_id in self.reviews:
            review = self.reviews[review_id]
            # Remove from place's reviews
            if review.place_id in self.places:
                place = self.places[review.place_id]
                place.reviews = [r for r in place.reviews if r.id != review_id]
            
            del self.reviews[review_id]
            return True
        return False


# Create instance
facade_final = HBnBFacadeFinal()
