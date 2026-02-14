#!/usr/bin/env python3
"""Comprehensive API test"""
import json
import requests
import time
import sys

BASE_URL = "http://localhost:5000/api/v1"

def test_endpoint(method, endpoint, data=None, expected_status=200):
    """Test an endpoint"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        else:
            print(f"Unknown method: {method}")
            return None
        
        print(f"{method} {endpoint}: {response.status_code}")
        
        if response.status_code != expected_status:
            print(f"  Expected {expected_status}, got {response.status_code}")
            if response.text:
                print(f"  Response: {response.text[:200]}")
        
        if response.text:
            try:
                return response.json()
            except:
                return response.text
        return None
        
    except requests.exceptions.ConnectionError:
        print(f"  Connection error - is server running?")
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None

def main():
    print("=" * 70)
    print("COMPREHENSIVE API TEST")
    print("=" * 70)
    
    # Wait a bit for server
    print("Waiting for server to be ready...")
    time.sleep(2)
    
    # 1. Get all places
    print("\n1. Testing GET /places/")
    places = test_endpoint("GET", "/places/")
    if places:
        print(f"  Found {len(places) if isinstance(places, list) else 0} places")
    
    # 2. Get a specific place if available
    if places and isinstance(places, list) and len(places) > 0:
        place_id = places[0].get('id')
        print(f"\n2. Testing GET /places/{place_id}")
        place = test_endpoint("GET", f"/places/{place_id}")
        if place:
            print(f"  Place: {place.get('title')} - ${place.get('price')}")
    
    # 3. Create a new place
    print("\n3. Testing POST /places/")
    # Get a user ID first
    if places and isinstance(places, list) and len(places) > 0:
        user_id = places[0].get('owner_id')
    else:
        # Use sample user ID from server output
        user_id = "212f2e51-0933-4e4f-a9c3-d756288593f6"
    
    new_place_data = {
        "title": "Beach House Test",
        "description": "Lovely beach house for testing",
        "price": 300.0,
        "latitude": 34.0522,
        "longitude": -118.2437,
        "owner_id": user_id,
        "amenities": []
    }
    
    new_place = test_endpoint("POST", "/places/", new_place_data, 201)
    if new_place:
        new_place_id = new_place.get('id')
        print(f"  Created: {new_place.get('title')} (ID: {new_place_id})")
        
        # 4. Update the place
        print(f"\n4. Testing PUT /places/{new_place_id}")
        update_data = {
            "title": "Updated Beach House",
            "price": 350.0
        }
        updated = test_endpoint("PUT", f"/places/{new_place_id}", update_data)
        if updated:
            print(f"  Updated successfully")
    
    # 5. Get all reviews
    print("\n5. Testing GET /reviews/")
    reviews = test_endpoint("GET", "/reviews/")
    if reviews:
        print(f"  Found {len(reviews) if isinstance(reviews, list) else 0} reviews")
    
    # 6. Create a review if we have a place and user
    print("\n6. Testing POST /reviews/")
    if places and isinstance(places, list) and len(places) > 0:
        place_id = places[0].get('id')
        # Get a different user for review (not the owner)
        # In sample data, we have 2 users
        user_ids = ["212f2e51-0933-4e4f-a9c3-d756288593f6", "716810de-7dc4-48ac-86c9-7fa8d2e62d8b"]
        reviewer_id = user_ids[1] if len(user_ids) > 1 else user_ids[0]
        
        review_data = {
            "text": "This is a test review created via API",
            "rating": 4,
            "user_id": reviewer_id,
            "place_id": place_id
        }
        
        new_review = test_endpoint("POST", "/reviews/", review_data, 201)
        if new_review:
            review_id = new_review.get('id')
            print(f"  Created review: {new_review.get('text')[:50]}...")
            
            # 7. Get place reviews
            print(f"\n7. Testing GET /places/{place_id}/reviews")
            place_reviews = test_endpoint("GET", f"/places/{place_id}/reviews")
            if place_reviews:
                print(f"  Place has {len(place_reviews)} reviews")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETED")
    print("=" * 70)

if __name__ == "__main__":
    main()
