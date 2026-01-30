#!/usr/bin/env python3
"""Test the complete API"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from services.facade import facade

# Create app
app = create_app()

print("=" * 70)
print("HBnB API Test Server")
print("=" * 70)
print(f"\nSample data loaded:")
print(f"  Users: {len(facade.users)}")
print(f"  Places: {len(facade.places)}")
print(f"  Amenities: {len(facade.amenities)}")
print(f"  Reviews: {len(facade.reviews)}")

if facade.places:
    print(f"\nSample place IDs:")
    for place_id, place in list(facade.places.items())[:3]:
        print(f"  - {place_id}: {place.title}")

print("\n" + "=" * 70)
print("Available Endpoints:")
print("=" * 70)
print("""
PLACES:
  GET    /api/v1/places/                 - List all places
  POST   /api/v1/places/                 - Create a new place
  GET    /api/v1/places/<place_id>       - Get place details
  PUT    /api/v1/places/<place_id>       - Update a place
  GET    /api/v1/places/<place_id>/reviews - Get reviews for a place

REVIEWS:
  GET    /api/v1/reviews/                - List all reviews
  POST   /api/v1/reviews/                - Create a new review
  GET    /api/v1/reviews/<review_id>     - Get review details
  PUT    /api/v1/reviews/<review_id>     - Update a review
  DELETE /api/v1/reviews/<review_id>     - Delete a review

DOCUMENTATION:
  GET    /api/v1/docs                    - Swagger UI documentation
""")

print("\nTo test with curl:")
print("  curl http://localhost:5000/api/v1/places/")
print("  curl http://localhost:5000/api/v1/reviews/")
print("\nStarting server... (press Ctrl+C to stop)")
print("=" * 70)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
