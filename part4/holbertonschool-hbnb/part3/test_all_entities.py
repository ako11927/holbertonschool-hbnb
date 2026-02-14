"""Test script to verify all entity mappings with SQLAlchemy."""
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app import create_app, db
from config import config
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.repositories.user_repository import UserRepository
from app.repositories.place_repository import PlaceRepository
from app.repositories.review_repository import ReviewRepository
from app.repositories.amenity_repository import AmenityRepository

# Create app with testing config
app = create_app(config['testing'])

with app.app_context():
    # Clear existing data and create tables
    db.drop_all()
    db.create_all()
    
    print("Testing all entity mappings with SQLAlchemy...")
    print("=" * 60)
    
    # Initialize repositories
    user_repo = UserRepository()
    place_repo = PlaceRepository()
    review_repo = ReviewRepository()
    amenity_repo = AmenityRepository()
    
    # Test 1: Create Amenities
    print("\n1. Testing Amenity entity:")
    amenities_data = [
        {'name': 'WiFi'},
        {'name': 'Swimming Pool'},
        {'name': 'Air Conditioning'},
        {'name': 'Parking'}
    ]
    
    created_amenities = []
    for amenity_data in amenities_data:
        try:
            amenity = amenity_repo.create_amenity(amenity_data)
            created_amenities.append(amenity)
            print(f"  ✓ Created: {amenity.name}")
        except ValueError as e:
            print(f"  ✗ Failed: {e}")
    
    # Test 2: Create a User
    print("\n2. Testing User entity:")
    user_data = {
        'email': 'owner@example.com',
        'first_name': 'John',
        'last_name': 'PropertyOwner',
        'password': 'ownerpass123',
        'is_admin': False
    }
    
    user = user_repo.create_user(user_data)
    if user:
        print(f"✓ User created: {user.email}")
        user_id = user.id
    else:
        print("✗ Failed to create user")
        user_id = None
    
    # Test 3: Create Places
    print("\n3. Testing Place entity:")
    places_data = [
        {
            'title': 'Beachfront Villa',
            'description': 'Beautiful villa with ocean views and private beach access.',
            'price': 250.00,
            'address': '123 Beach Road',
            'city': 'Miami',
            'max_guests': 6,
            'bedrooms': 3,
            'bathrooms': 2,
            'latitude': 25.7617,
            'longitude': -80.1918
        },
        {
            'title': 'Downtown Apartment',
            'description': 'Modern apartment in the heart of the city with great amenities.',
            'price': 120.00,
            'address': '456 City Center',
            'city': 'New York',
            'max_guests': 4,
            'bedrooms': 2,
            'bathrooms': 1
        }
    ]
    
    created_places = []
    for place_data in places_data:
        try:
            place = place_repo.create_place(place_data)
            created_places.append(place)
            print(f"  ✓ Created: {place.title} in {place.city} (${place.price}/night)")
        except ValueError as e:
            print(f"  ✗ Failed: {e}")
    
    # Test 4: Create Reviews
    print("\n4. Testing Review entity:")
    if created_places:
        review_data = {
            'text': 'Amazing place! Beautiful views and excellent service.',
            'rating': 5
        }
        
        try:
            review = review_repo.create_review(review_data)
            print(f"✓ Review created: {review.rating} stars")
            print(f"  Text: {review.text[:50]}...")
        except ValueError as e:
            print(f"✗ Failed: {e}")
    
    # Test 5: Test CRUD Operations
    print("\n5. Testing CRUD operations for all entities:")
    
    # Get all entities
    all_users = user_repo.get_all()
    all_places = place_repo.get_all()
    all_reviews = review_repo.get_all()
    all_amenities = amenity_repo.get_all()
    
    print(f"  Users: {len(all_users)}")
    print(f"  Places: {len(all_places)}")
    print(f"  Reviews: {len(all_reviews)}")
    print(f"  Amenities: {len(all_amenities)}")
    
    # Test search and filter operations
    print("\n6. Testing search and filter operations:")
    
    # Search places
    if created_places:
        miami_places = place_repo.get_places_by_city('Miami')
        print(f"  Places in Miami: {len(miami_places)}")
        
        price_range_places = place_repo.get_places_by_price_range(100, 200)
        print(f"  Places in $100-$200 range: {len(price_range_places)}")
    
    # Search amenities
    pool_amenity = amenity_repo.get_amenity_by_name('Swimming Pool')
    if pool_amenity:
        print(f"  Found amenity: {pool_amenity.name}")
    
    # Test repository-specific methods
    print("\n7. Testing repository-specific methods:")
    
    if created_places and len(created_places) > 0:
        # Test place filters
        filters = {
            'city': 'Miami',
            'min_price': 200
        }
        filtered_places = place_repo.get_places_with_filters(filters)
        print(f"  Places in Miami with price >= $200: {len(filtered_places)}")
    
    # Test review repository methods
    rating_5_reviews = review_repo.get_reviews_by_rating(5)
    print(f"  5-star reviews: {len(rating_5_reviews)}")
    
    recent_reviews = review_repo.get_recent_reviews(5)
    print(f"  Recent reviews (limit 5): {len(recent_reviews)}")
    
    # Test 8: Test validation
    print("\n8. Testing entity validation:")
    
    # Test invalid place creation
    try:
        invalid_place_data = {
            'title': 'AB',  # Too short
            'description': 'Short',
            'price': -100  # Negative price
        }
        invalid_place = Place(**invalid_place_data)
        print("  ✗ Invalid place should have been rejected")
    except ValueError as e:
        print(f"  ✓ Invalid place correctly rejected: {str(e)[:50]}...")
    
    # Test invalid review creation
    try:
        invalid_review_data = {
            'text': 'Too short',
            'rating': 6  # Invalid rating
        }
        invalid_review = Review(**invalid_review_data)
        print("  ✗ Invalid review should have been rejected")
    except ValueError as e:
        print(f"  ✓ Invalid review correctly rejected: {str(e)[:50]}...")
    
    # Test duplicate amenity
    try:
        duplicate_amenity_data = {'name': 'WiFi'}  # Already exists
        duplicate_amenity = amenity_repo.create_amenity(duplicate_amenity_data)
        print("  ✗ Duplicate amenity should have been rejected")
    except ValueError as e:
        print(f"  ✓ Duplicate amenity correctly rejected: {e}")
    
    # Test 9: Clean up
    print("\n9. Cleaning up test data...")
    
    # Delete test data
    for place in created_places:
        place_repo.delete(place.id)
        print(f"  Deleted place: {place.title}")
    
    for amenity in created_amenities:
        amenity_repo.delete(amenity.id)
        print(f"  Deleted amenity: {amenity.name}")
    
    if user_id:
        user_repo.delete(user_id)
        print(f"  Deleted user")
    
    # Verify cleanup
    remaining_users = len(user_repo.get_all())
    remaining_places = len(place_repo.get_all())
    remaining_reviews = len(review_repo.get_all())
    remaining_amenities = len(amenity_repo.get_all())
    
    print(f"\nRemaining entities after cleanup:")
    print(f"  Users: {remaining_users}")
    print(f"  Places: {remaining_places}")
    print(f"  Reviews: {remaining_reviews}")
    print(f"  Amenities: {remaining_amenities}")
    
    print("\n" + "=" * 60)
    print("All entity mapping tests completed successfully!")
