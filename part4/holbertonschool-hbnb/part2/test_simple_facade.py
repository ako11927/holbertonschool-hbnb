#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing simple facade...")

try:
    from services.facade_simple import facade_simple
    print(f"✓ Simple facade loaded")
    print(f"  Users: {len(facade_simple.users)}")
    print(f"  Places: {len(facade_simple.places)}")
    
    # If we have users, test creating a place
    if facade_simple.users:
        user_id = list(facade_simple.users.keys())[0]
        print(f"\nTest user ID: {user_id}")
        
        place_data = {
            'title': 'Test House',
            'description': 'Test description',
            'price': '150.0',
            'latitude': '40.7128',
            'longitude': '-74.0060',
            'owner_id': user_id,
            'amenities': []
        }
        
        place = facade_simple.create_place(place_data)
        if place:
            print(f"✓ Created place: {place.title}")
            print(f"  ID: {place.id}")
            print(f"  Price: ${place.price}")
            
            # Test getting it back
            retrieved = facade_simple.get_place(place.id)
            print(f"✓ Retrieved: {retrieved.title if retrieved else 'No'}")
        else:
            print("✗ Failed to create place")
    else:
        print("⚠ No users in facade")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
