#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from services import facade

app = create_app()

print("=" * 70)
print("HBnB API Server - FINAL TEST")
print("=" * 70)

if facade:
    print(f"\nFacade data:")
    print(f"  Users: {len(facade.users)}")
    print(f"  Places: {len(facade.places)}")
    print(f"  Amenities: {len(facade.amenities)}")
    print(f"  Reviews: {len(facade.reviews)}")
    
    if facade.places:
        print(f"\nSample places:")
        for place_id, place in list(facade.places.items())[:2]:
            print(f"  - {place.title}: ${place.price}/night")
    
    if facade.users:
        print(f"\nSample users (for testing):")
        for user_id, user in list(facade.users.items())[:2]:
            print(f"  - {user_id}: {user.first_name} {user.last_name}")
else:
    print("\n⚠ No facade available")

print("\n" + "=" * 70)
print("Server starting on http://localhost:5000")
print("API docs: http://localhost:5000/api/v1/docs")
print("=" * 70)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
