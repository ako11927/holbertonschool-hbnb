#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing main facade...")

try:
    # Update services/__init__.py to use main facade
    import services
    # Force reload
    if 'facade' in dir(services):
        del services.facade
    
    # Update to use main facade
    from services.facade import facade
    
    print(f"✓ Main facade loaded")
    print(f"  Users: {len(facade.users)}")
    print(f"  Places: {len(facade.places)}")
    print(f"  Amenities: {len(facade.amenities)}")
    print(f"  Reviews: {len(facade.reviews)}")
    
    # Test creating a place
    if facade.users:
        user_id = list(facade.users.keys())[0]
        print(f"\nTest with user: {user_id}")
        
        place_data = {
            'title': 'Test Place via Main Facade',
            'description': 'Created via main facade',
            'price': 175.0,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'owner_id': user_id,
            'amenities': []
        }
        
        try:
            place = facade.create_place(place_data)
            print(f"✓ Created place: {place.title}")
            print(f"  ID: {place.id}")
            print(f"  Price: ${place.price}")
            
            # Test getting all places
            all_places = facade.get_all_places()
            print(f"✓ Total places: {len(all_places)}")
            
        except Exception as e:
            print(f"✗ Error creating place: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("⚠ No users in facade")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
