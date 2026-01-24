#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")

# Test model imports
try:
    from models import User, Place, Amenity, Review
    print("✓ Imported all models from models package")
    
    # Create instances
    user = User(first_name="Test", last_name="User", email="test@example.com")
    place = Place(title="Test Place", price=100.0, latitude=40.0, longitude=-70.0)
    amenity = Amenity(name="Test Amenity")
    review = Review(text="Test review", rating=5)
    
    print(f"✓ Created: {user.first_name} {user.last_name}")
    print(f"✓ Created: {place.title}")
    print(f"✓ Created: {amenity.name}")
    print(f"✓ Created: review with rating {review.rating}")
except Exception as e:
    print(f"✗ Error importing models: {e}")
    import traceback
    traceback.print_exc()

# Test facade
print("\nTesting facade...")
try:
    from services.facade import facade
    print(f"✓ Facade loaded")
    print(f"  Users: {len(facade.users)}")
    print(f"  Places: {len(facade.places)}")
    print(f"  Amenities: {len(facade.amenities)}")
    print(f"  Reviews: {len(facade.reviews)}")
    
    # Test creating a place
    if facade.users:
        user_id = list(facade.users.keys())[0]
        place_data = {
            'title': 'Beach House',
            'description': 'Beautiful beach house',
            'price': 200.0,
            'latitude': 34.0522,
            'longitude': -118.2437,
            'owner_id': user_id,
            'amenities': []
        }
        place = facade.create_place(place_data)
        print(f"✓ Created place: {place.title} (${place.price}/night)")
        print(f"  Total places now: {len(facade.places)}")
    else:
        print("⚠ No users in facade - sample data not loaded")
except Exception as e:
    print(f"✗ Error with facade: {e}")
    import traceback
    traceback.print_exc()
