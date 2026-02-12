"""Test script to verify relationships between entities."""
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
    
    print("Testing relationships between entities...")
    print("=" * 60)
    
    # Initialize repositories
    user_repo = UserRepository()
    place_repo = PlaceRepository()
    review_repo = ReviewRepository()
    amenity_repo = AmenityRepository()
    
    # Create test data with relationships
    print("\n1. Creating test data with relationships:")
    
    # Create users
    print("\n  Creating users...")
    owner_data = {
        'email': 'owner@example.com',
        'first_name': 'John',
        'last_name': 'PropertyOwner',
        'password': 'ownerpass123',
        'is_admin': False
    }
    owner = user_repo.create_user(owner_data)
    
    reviewer_data = {
        'email': 'reviewer@example.com',
        'first_name': 'Jane',
        'last_name': 'Traveler',
        'password': 'reviewerpass123',
        'is_admin': False
    }
    reviewer = user_repo.create_user(reviewer_data)
    
    print(f"  ✓ Owner: {owner.email}")
    print(f"  ✓ Reviewer: {reviewer.email}")
    
    # Create amenities
    print("\n  Creating amenities...")
    amenities = ['WiFi', 'Swimming Pool', 'Air Conditioning', 'Parking', 'Kitchen']
    created_amenities = []
    for amenity_name in amenities:
        amenity = amenity_repo.create_amenity({'name': amenity_name})
        if amenity:
            created_amenities.append(amenity)
            print(f"    ✓ {amenity.name}")
    
    # Create place with owner relationship
    print("\n  Creating place with owner relationship...")
    place_data = {
        'title': 'Luxury Villa',
        'description': 'A beautiful villa with all modern amenities and stunning views.',
        'price': 350.00,
        'address': '456 Luxury Lane',
        'city': 'Beverly Hills',
        'max_guests': 8,
        'bedrooms': 4,
        'bathrooms': 3,
        'owner_id': owner.id,
        'amenities': [amenity.id for amenity in created_amenities[:3]]  # Add first 3 amenities
    }
    
    place = place_repo.create_place(place_data)
    print(f"  ✓ Place: {place.title} (Owner: {place.owner.first_name})")
    print(f"    Amenities: {[a.name for a in place.amenities]}")
    
    # Create another place for the same owner
    print("\n  Creating another place for same owner...")
    place2_data = {
        'title': 'Beach House',
        'description': 'Cozy beach house with ocean view.',
        'price': 200.00,
        'address': '789 Beach Road',
        'city': 'Miami',
        'max_guests': 6,
        'bedrooms': 3,
        'bathrooms': 2,
        'owner_id': owner.id,
        'amenities': [created_amenities[0].id, created_amenities[4].id]  # WiFi and Kitchen
    }
    
    place2 = place_repo.create_place(place2_data)
    print(f"  ✓ Place: {place2.title} (Owner: {place2.owner.first_name})")
    
    # Create reviews with relationships
    print("\n2. Creating reviews with relationships:")
    
    # Review 1: Reviewer reviews first place
    review1_data = {
        'text': 'Absolutely amazing villa! The amenities were top-notch and the service was exceptional.',
        'rating': 5,
        'user_id': reviewer.id,
        'place_id': place.id
    }
    
    try:
        review1 = review_repo.create_review(review1_data)
        print(f"  ✓ Review 1: {review1.rating} stars for {review1.place.title}")
        print(f"    By: {review1.user.first_name}")
    except ValueError as e:
        print(f"  ✗ Review 1 failed: {e}")
    
    # Review 2: Reviewer reviews second place
    review2_data = {
        'text': 'Great beach house! Perfect location and very clean.',
        'rating': 4,
        'user_id': reviewer.id,
        'place_id': place2.id
    }
    
    try:
        review2 = review_repo.create_review(review2_data)
        print(f"  ✓ Review 2: {review2.rating} stars for {review2.place.title}")
        print(f"    By: {review2.user.first_name}")
    except ValueError as e:
        print(f"  ✗ Review 2 failed: {e}")
    
    # Test 3: Verify bidirectional relationships
    print("\n3. Testing bidirectional relationships:")
    
    # User -> Places (One-to-Many)
    print("\n  User -> Places relationship:")
    print(f"  {owner.first_name} owns {len(owner.places)} place(s):")
    for p in owner.places:
        print(f"    - {p.title} in {p.city} (${p.price}/night)")
    
    # User -> Reviews (One-to-Many)
    print("\n  User -> Reviews relationship:")
    print(f"  {reviewer.first_name} wrote {len(reviewer.reviews)} review(s):")
    for r in reviewer.reviews:
        print(f"    - {r.rating} stars for {r.place.title}")
    
    # Place -> Reviews (One-to-Many)
    print("\n  Place -> Reviews relationship:")
    print(f"  {place.title} has {len(place.reviews)} review(s):")
    for r in place.reviews:
        print(f"    - {r.rating} stars by {r.user.first_name}")
    
    # Place -> Amenities (Many-to-Many)
    print("\n  Place -> Amenities relationship:")
    print(f"  {place.title} has {len(place.amenities)} amenity/ies:")
    for a in place.amenities:
        print(f"    - {a.name}")
    
    # Amenity -> Places (Many-to-Many)
    print("\n  Amenity -> Places relationship:")
    for amenity in created_amenities:
        print(f"  {amenity.name} is available in {len(amenity.places)} place(s):")
        for p in amenity.places:
            print(f"    - {p.title}")
    
    # Test 4: Test repository relationship methods
    print("\n4. Testing repository relationship methods:")
    
    # Get user with relationships
    user_with_rels = user_repo.get_user_with_relationships(owner.id)
    print(f"  User with relationships loaded: {user_with_rels.first_name}")
    print(f"    Places count: {len(user_with_rels.places)}")
    print(f"    Reviews count: {len(user_with_rels.reviews)}")
    
    # Get place with relationships
    place_with_rels = place_repo.get_place_with_relationships(place.id)
    print(f"\n  Place with relationships loaded: {place_with_rels.title}")
    print(f"    Owner: {place_with_rels.owner.first_name}")
    print(f"    Reviews count: {len(place_with_rels.reviews)}")
    print(f"    Amenities count: {len(place_with_rels.amenities)}")
    
    # Get review with relationships
    if review1:
        review_with_rels = review_repo.get_review_with_relationships(review1.id)
        print(f"\n  Review with relationships loaded: {review_with_rels.rating} stars")
        print(f"    User: {review_with_rels.user.first_name}")
        print(f"    Place: {review_with_rels.place.title}")
    
    # Test 5: Test cascade operations
    print("\n5. Testing cascade operations:")
    
    # Test adding/removing amenities dynamically
    print("\n  Testing dynamic many-to-many relationships:")
    
    # Add an amenity to place
    new_amenity = amenity_repo.create_amenity({'name': 'Hot Tub'})
    place = place_repo.add_amenity_to_place(place.id, new_amenity.id)
    print(f"  ✓ Added 'Hot Tub' to {place.title}")
    print(f"    Place now has {len(place.amenities)} amenities")
    
    # Remove an amenity from place
    place = place_repo.remove_amenity_from_place(place.id, created_amenities[0].id)
    print(f"  ✓ Removed 'WiFi' from {place.title}")
    print(f"    Place now has {len(place.amenities)} amenities")
    
    # Test 6: Test cascade delete
    print("\n6. Testing cascade delete:")
    
    # Count before deletion
    reviews_before = len(review_repo.get_all())
    places_before = len(place_repo.get_all())
    
    print(f"  Before deleting user '{owner.first_name}':")
    print(f"    Total reviews: {reviews_before}")
    print(f"    Total places: {places_before}")
    
    # Delete owner (should cascade delete places and their reviews)
    user_repo.delete(owner.id)
    
    # Count after deletion
    reviews_after = len(review_repo.get_all())
    places_after = len(place_repo.get_all())
    
    print(f"\n  After deleting user '{owner.first_name}':")
    print(f"    Total reviews: {reviews_after}")
    print(f"    Total places: {places_after}")
    print(f"    Reviews deleted: {reviews_before - reviews_after}")
    print(f"    Places deleted: {places_before - places_after}")
    
    # Verify the owner's places were deleted
    owner_places = place_repo.get_places_by_owner(owner.id)
    print(f"    Places still owned by deleted user: {len(owner_places)}")
    
    # Test 7: Test duplicate review prevention
    print("\n7. Testing duplicate review prevention:")
    
    if reviewer and place2:
        duplicate_review_data = {
            'text': 'Another review for the same place.',
            'rating': 3,
            'user_id': reviewer.id,
            'place_id': place2.id
        }
        
        try:
            duplicate_review = review_repo.create_review(duplicate_review_data)
            print("  ✗ Duplicate review should have been rejected")
        except ValueError as e:
            print(f"  ✓ Duplicate review correctly rejected: {e}")
    
    # Test 8: Test querying through relationships
    print("\n8. Testing advanced relationship queries:")
    
    # Get average rating for remaining place
    if place2:
        avg_rating = review_repo.get_average_rating_for_place(place2.id)
        print(f"  Average rating for {place2.title}: {avg_rating:.1f}")
    
    # Get places with specific amenities
    wifi_amenity = amenity_repo.get_amenity_by_name('WiFi')
    if wifi_amenity:
        print(f"\n  Places with 'WiFi' amenity: {len(wifi_amenity.places)}")
        for p in wifi_amenity.places:
            print(f"    - {p.title}")
    
    # Get reviews by specific user
    user_reviews = review_repo.get_reviews_by_user(reviewer.id)
    print(f"\n  Reviews by {reviewer.first_name}: {len(user_reviews)}")
    for r in user_reviews:
        print(f"    - {r.rating} stars for {r.place.title if r.place else 'deleted place'}")
    
    print("\n" + "=" * 60)
    print("Relationship mapping tests completed successfully!")
