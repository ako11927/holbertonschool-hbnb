#!/usr/bin/env python3
"""Simple test script for Place and Review endpoints"""

import json
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.services import facade

def test_facade_directly():
    """Test facade methods directly"""
    print("=" * 60)
    print("Testing Facade Methods Directly")
    print("=" * 60)
    
    # Test 1: Check if facade has users
    print(f"\n1. Number of users: {len(facade.users)}")
    print(f"2. Number of places: {len(facade.places)}")
    print(f"3. Number of amenities: {len(facade.amenities)}")
    print(f"4. Number of reviews: {len(facade.reviews)}")
    
    # Test 2: Get all places
    places = facade.get_all_places()
    print(f"\n5. Sample places in system: {len(places)}")
    for i, place in enumerate(places[:3], 1):
        print(f"   Place {i}: {place.title} (ID: {place.id})")
    
    # Test 3: Create a new place
    print("\n6. Testing create_place method...")
    try:
        # Get a user ID for testing
        user_id = list(facade.users.keys())[0]
        
        new_place_data = {
            "title": "Test Beach House",
            "description": "A beautiful beach house",
            "price": 200.0,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner_id": user_id,
            "amenities": []
        }
        
        new_place = facade.create_place(new_place_data)
        print(f"   Created place: {new_place.title} (ID: {new_place.id})")
        
        # Test 4: Get the created place
        retrieved_place = facade.get_place(new_place.id)
        print(f"   Retrieved place: {retrieved_place.title}")
        
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 5: Create a review
    print("\n7. Testing create_review method...")
    try:
        # Get user and place IDs
        user_id = list(facade.users.keys())[1] if len(facade.users) > 1 else list(facade.users.keys())[0]
        place_id = list(facade.places.keys())[0]
        
        review_data = {
            "text": "Excellent place! Would stay again.",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id
        }
        
        review = facade.create_review(review_data)
        print(f"   Created review: {review.text[:50]}...")
        
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == '__main__':
    print("Starting tests...")
    test_facade_directly()
    print("\n" + "=" * 60)
    print("Tests completed!")
    print("=" * 60)
