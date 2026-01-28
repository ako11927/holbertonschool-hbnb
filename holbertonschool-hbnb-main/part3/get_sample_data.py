#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.facade import facade

print("Sample data in facade:")
print(f"Users: {len(facade.users)}")
for user_id, user in facade.users.items():
    print(f"  {user_id}: {user.first_name} {user.last_name} ({user.email})")

print(f"\nPlaces: {len(facade.places)}")
for place_id, place in facade.places.items():
    print(f"  {place_id}: {place.title} (${place.price})")

print(f"\nAmenities: {len(facade.amenities)}")
for amenity_id, amenity in facade.amenities.items():
    print(f"  {amenity_id}: {amenity.name}")

if facade.users:
    print(f"\nUse this user_id for testing: {list(facade.users.keys())[0]}")
