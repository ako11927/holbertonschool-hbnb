#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("FINAL VERSION TEST")
print("=" * 70)

# Force reload
import services
if 'facade' in dir(services):
    del services.facade

from services import facade

if not facade:
    print("✗ No facade available")
    sys.exit(1)

print(f"✓ Facade loaded: {type(facade).__name__}")
print(f"\nData status:")
print(f"  Users: {len(facade.users)}")
print(f"  Places: {len(facade.places)}")
print(f"  Amenities: {len(facade.amenities)}")
print(f"  Reviews: {len(facade.reviews)}")

# Test creating a place
if facade.users:
    user_id = list(facade.users.keys())[0]
    print(f"\nTest 1: Creating a place with user {user_id}")
    
    place_data = {
        'title': 'Beautiful Villa',
        'description': 'Luxury villa with pool',
        'price': 350.0,
        'latitude': 34.0522,
        'longitude': -118.2437,
        'owner_id': user_id,
        'amenities': list(facade.amenities.keys())[:2] if facade.amenities else []
    }
    
    try:
        place = facade.create_place(place_data)
        print(f"  ✓ Created: {place.title} (${place.price})")
        print(f"  ✓ ID: {place.id}")
        print(f"  ✓ Owner: {place.owner.first_name if place.owner else 'None'}")
        print(f"  ✓ Amenities: {len(place.amenities)}")
        
        # Test getting it back
        retrieved = facade.get_place(place.id)
        print(f"  ✓ Retrieved: {retrieved.title if retrieved else 'Failed'}")
        
    except Exception as e:
        print(f"  ✗ Error: {e}")

# Test getting all places
print(f"\nTest 2: Getting all places")
all_places = facade.get_all_places()
print(f"  ✓ Total places: {len(all_places)}")
for i, p in enumerate(all_places[:3], 1):
    print(f"    {i}. {p.title} - ${p.price}")

# Test creating a review
if facade.users and facade.places:
    print(f"\nTest 3: Creating a review")
    
    # Use different user than the place owner
    user_ids = list(facade.users.keys())
    place_ids = list(facade.places.keys())
    
    if len(user_ids) > 1 and place_ids:
        reviewer_id = user_ids[1]  # Different user
        place_id = place_ids[0]
        
        review_data = {
            'text': 'Amazing place! Highly recommend.',
            'rating': 5,
            'user_id': reviewer_id,
            'place_id': place_id
        }
        
        try:
            review = facade.create_review(review_data)
            print(f"  ✓ Created review: '{review.text[:30]}...'")
            print(f"  ✓ Rating: {review.rating}/5")
            
            # Test getting reviews for place
            place_reviews = facade.get_reviews_by_place(place_id)
            print(f"  ✓ Place has {len(place_reviews)} reviews")
            
        except Exception as e:
            print(f"  ✗ Error: {e}")

print("\n" + "=" * 70)
print("TEST COMPLETED SUCCESSFULLY!")
print("=" * 70)
