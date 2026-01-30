#!/usr/bin/env python3
"""Run the final API server"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from services import facade

app = create_app()

print("=" * 70)
print("HBnB API SERVER - FINAL VERSION")
print("=" * 70)

print(f"\nServer initialized with:")
print(f"  Users: {len(facade.users)}")
print(f"  Places: {len(facade.places)}")
print(f"  Amenities: {len(facade.amenities)}")
print(f"  Reviews: {len(facade.reviews)}")

print(f"\nSample place IDs (for testing):")
for place_id, place in list(facade.places.items())[:3]:
    print(f"  - {place_id}: {place.title} (${place.price})")

print(f"\nSample user IDs (for testing POST requests):")
for user_id, user in list(facade.users.items())[:3]:
    print(f"  - {user_id}: {user.first_name} {user.last_name}")

print("\n" + "=" * 70)
print("ENDPOINTS:")
print("=" * 70)
print("""
PLACES:
  GET    /api/v1/places/                  - List all places
  POST   /api/v1/places/                  - Create new place
  GET    /api/v1/places/<id>              - Get place details
  PUT    /api/v1/places/<id>              - Update place
  GET    /api/v1/places/<id>/reviews      - Get place reviews

REVIEWS:
  GET    /api/v1/reviews/                 - List all reviews
  POST   /api/v1/reviews/                 - Create new review
  GET    /api/v1/reviews/<id>             - Get review details
  PUT    /api/v1/reviews/<id>             - Update review
  DELETE /api/v1/reviews/<id>             - Delete review

DOCS:
  GET    /api/v1/docs                     - Swagger UI
""")

print("\n" + "=" * 70)
print("Server starting on http://localhost:5000")
print("Press Ctrl+C to stop")
print("=" * 70)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
