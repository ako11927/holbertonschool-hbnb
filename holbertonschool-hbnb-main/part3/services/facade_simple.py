import uuid
from datetime import datetime

# Simple facade without complex imports at module level
class HBnBFacadeSimple:
    def __init__(self):
        self.users = {}
        self.places = {}
        self.amenities = {}
        self.reviews = {}
        self._load_sample_data()
    
    def _load_sample_data(self):
        """Load sample data - import models inside method"""
        try:
            # Import here to avoid circular imports
            from models.user import User
            from models.amenity import Amenity
            from models.place import Place
            from models.review import Review
            
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
            
            self.amenities[wifi.id] = wifi
            self.amenities[ac.id] = ac
            
            # Create sample place - set attributes directly to avoid property issues
            place1 = Place()
            place1.id = str(uuid.uuid4())
            place1.title = "Cozy Apartment"
            place1.description = "A nice place to stay"
            
            # Set private attributes directly to avoid property validation during init
            place1._price = 100.0
            place1._latitude = 37.7749
            place1._longitude = -122.4194
            
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
            
            print(f"✓ Loaded {len(self.users)} users, {len(self.places)} places, "
                  f"{len(self.amenities)} amenities, {len(self.reviews)} reviews")
            
        except ImportError as e:
            print(f"✗ Error importing models: {e}")
            import traceback
            traceback.print_exc()
            print("Creating empty data structures...")
            # Create empty dictionaries
            self.users = {}
            self.places = {}
            self.amenities = {}
            self.reviews = {}
        except Exception as e:
            print(f"✗ Error loading sample data: {e}")
            import traceback
            traceback.print_exc()
    
    def create_place(self, data):
        """Create a new place"""
        try:
            from models.place import Place
            
            # Validate
            if 'owner_id' not in data:
                return None
            
            # Create place
            place = Place()
            place.id = str(uuid.uuid4())
            place.title = data.get('title', '')
            place.description = data.get('description', '')
            
            # Set price using property setter
            try:
                place.price = float(data.get('price', 0))
            except (ValueError, TypeError):
                place.price = 0.0
            
            # Set latitude using property setter
            try:
                place.latitude = float(data.get('latitude', 0))
            except (ValueError, TypeError):
                place.latitude = 0.0
            
            # Set longitude using property setter
            try:
                place.longitude = float(data.get('longitude', 0))
            except (ValueError, TypeError):
                place.longitude = 0.0
            
            place.owner_id = data.get('owner_id')
            
            # Set owner if exists
            if place.owner_id in self.users:
                place.owner = self.users[place.owner_id]
            
            # Add amenities
            for amenity_id in data.get('amenities', []):
                if amenity_id in self.amenities:
                    place.amenities.append(self.amenities[amenity_id])
            
            self.places[place.id] = place
            return place
            
        except Exception as e:
            print(f"Error creating place: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_place(self, place_id):
        """Get place by ID"""
        return self.places.get(place_id)
    
    def get_all_places(self):
        """Get all places"""
        return list(self.places.values())
    
    def update_place(self, place_id, data):
        """Update a place"""
        place = self.places.get(place_id)
        if not place:
            return None
        
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
        
        return place
    
    def create_review(self, data):
        """Create a new review"""
        try:
            from models.review import Review
            
            # Validate
            required = ['text', 'rating', 'user_id', 'place_id']
            for field in required:
                if field not in data:
                    return None
            
            rating = int(data['rating'])
            if not 1 <= rating <= 5:
                return None
            
            # Create review
            review = Review()
            review.id = str(uuid.uuid4())
            review.text = data['text']
            review.rating = rating
            review.user_id = data['user_id']
            review.place_id = data['place_id']
            
            # Set user and place if they exist
            if review.user_id in self.users:
                review.user = self.users[review.user_id]
            if review.place_id in self.places:
                review.place = self.places[review.place_id]
            
            self.reviews[review.id] = review
            return review
            
        except Exception as e:
            print(f"Error creating review: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_review(self, review_id):
        """Get review by ID"""
        return self.reviews.get(review_id)
    
    def get_all_reviews(self):
        """Get all reviews"""
        return list(self.reviews.values())
    
    def get_reviews_by_place(self, place_id):
        """Get reviews for a place"""
        return [r for r in self.reviews.values() if r.place_id == place_id]
    
    def update_review(self, review_id, data):
        """Update a review"""
        review = self.reviews.get(review_id)
        if not review:
            return None
        
        if 'text' in data:
            review.text = data['text']
        if 'rating' in data:
            try:
                rating = int(data['rating'])
                if 1 <= rating <= 5:
                    review.rating = rating
            except (ValueError, TypeError):
                pass
        
        return review
    
    def delete_review(self, review_id):
        """Delete a review"""
        if review_id in self.reviews:
            del self.reviews[review_id]
            return True
        return False


# Create instance
facade_simple = HBnBFacadeSimple()
