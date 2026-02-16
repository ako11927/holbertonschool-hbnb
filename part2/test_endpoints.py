#!/usr/bin/env python3
"""Test script for Place and Review endpoints"""

import json
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.services import facade

def test_place_endpoints():
    """Test place endpoints"""
    app = create_app()
    client = app.test_client()
    
    print("=" * 60)
    print("Testing Place Endpoints")
    print("=" * 60)
    
    # Get sample user ID for testing
    sample_users = list(facade.users.values())
    if not sample_users:
        print("No sample users found!")
        return
    
    owner_id = sample_users[0].id
    
    # 1. Test GET all places
    print("\n1. Testing GET /api/v1/places/")
    response = client.get('/api/v1/places/')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        places = json.loads(response.data)
        print(f"Found {len(places)} places")
    
    # 2. Test POST create place
    print("\n2. Testing POST /api/v1/places/")
    place_data = {
        "title": "Test Place",
        "description": "A test place",
        "price": 99.99,
        "latitude": 40.7128,
        "longitude": -74.0060,
        "owner_id": owner_id,
        "amenities": []
    }
    response = client.post('/api/v1/places/', 
                          json=place_data,
                          content_type='application/json')
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        place = json.loads(response.data)
        print(f"Created place with ID: {place.get('id')}")
        place_id = place.get('id')
    
    # 3. Test GET specific place
    print("\n3. Testing GET /api/v1/places/<place_id>")
    if 'place_id' in locals():
        response = client.get(f'/api/v1/places/{place_id}')
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            place = json.loads(response.data)
            print(f"Retrieved place: {place.get('title')}")
    
    # 4. Test PUT update place
    print("\n4. Testing PUT /api/v1/places/<place_id>")
    if 'place_id' in locals():
        update_data = {
            "title": "Updated Test Place",
            "price": 150.0
        }
        response = client.put(f'/api/v1/places/{place_id}',
                             json=update_data,
                             content_type='application/json')
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("Place updated successfully")

def test_review_endpoints():
    """Test review endpoints"""
    app = create_app()
    client = app.test_client()
    
    print("\n" + "=" * 60)
    print("Testing Review Endpoints")
    print("=" * 60)
    
    # Get sample user and place IDs for testing
    sample_users = list(facade.users.values())
    sample_places = list(facade.places.values())
    
    if not sample_users or not sample_places:
        print("No sample data found!")
        return
    
    user_id = sample_users[1].id if len(sample_users) > 1 else sample_users[0].id
    place_id = sample_places[0].id
    
    # 1. Test POST create review
    print("\n1. Testing POST /api/v1/reviews/")
    review_data = {
        "text": "Great place for testing!",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    }
    response = client.post('/api/v1/reviews/',
                          json=review_data,
                          content_type='application/json')
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        review = json.loads(response.data)
        print(f"Created review with ID: {review.get('id')}")
        review_id = review.get('id')
    
    # 2. Test GET all reviews
    print("\n2. Testing GET /api/v1/reviews/")
    response = client.get('/api/v1/reviews/')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        reviews = json.loads(response.data)
        print(f"Found {len(reviews)} reviews")
    
    # 3. Test GET place reviews
    print("\n3. Testing GET /api/v1/places/<place_id>/reviews")
    response = client.get(f'/api/v1/places/{place_id}/reviews')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        reviews = json.loads(response.data)
        print(f"Found {len(reviews)} reviews for place")
    
    # 4. Test DELETE review
    print("\n4. Testing DELETE /api/v1/reviews/<review_id>")
    if 'review_id' in locals():
        response = client.delete(f'/api/v1/reviews/{review_id}')
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("Review deleted successfully")

if __name__ == '__main__':
    print("Starting API tests...")
    test_place_endpoints()
    test_review_endpoints()
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)
