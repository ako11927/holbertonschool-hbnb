#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing facade with fixed imports...")

try:
    from services.facade import facade
    print(f"✓ Facade loaded")
    print(f"  Users: {len(facade.users)}")
    print(f"  Places: {len(facade.places)}")
    print(f"  Amenities: {len(facade.amenities)}")
    print(f"  Reviews: {len(facade.reviews)}")
    
    # Test creating a place if we have users
    if facade.users:
        user_id = list(facade.users.keys())[0]
        print(f"\nCreating test place with user: {user_id}")
        
        place_data = {
            'title': 'Beach House',
            'description': 'Beautiful beach house',
            'price': 200.0,
            'latitude': 34.0522,
            'longitude': -118.2437,
            'owner_id': user_id,
            'amenities': []
        }
        
        try:
            place = facade.create_place(place_data)
            print(f"✓ Created place: {place.title} (${place.price}/night)")
            print(f"  Place ID: {place.id}")
            print(f"  Total places now: {len(facade.places)}")
            
            # Test getting the place
            retrieved = facade.get_place(place.id)
            print(f"✓ Retrieved place: {retrieved.title if retrieved else 'Not found'}")
            
            # Test getting all places
            all_places = facade.get_all_places()
            print(f"✓ Got all places: {len(all_places)} total")
            
        except Exception as e:
            print(f"✗ Error creating place: {e}")
    else:
        print("\n⚠ No users in facade - checking if we can create one")
        # Try to manually add a user
        from models.user import User
        import uuid
        test_user = User(
            id=str(uuid.uuid4()),
            first_name="Test",
            last_name="User",
            email="test@example.com"
        )
        facade.users[test_user.id] = test_user
        print(f"✓ Created test user: {test_user.id}")
        
except Exception as e:
    print(f"✗ Error with facade: {e}")
    import traceback
    traceback.print_exc()
