#!/usr/bin/env python3
"""Test Amenity endpoints for Task 03."""
import json
from app import create_app

app = create_app()

print("=== Testing Amenity Endpoints (Task 03) ===")

with app.test_client() as client:
    # Test 1: Create an amenity (POST)
    print("\n1. Testing POST /api/v1/amenities/ - Create amenity")
    amenity_data = {
        'name': 'Wi-Fi'
    }
    
    response = client.post('/api/v1/amenities/', 
                          data=json.dumps(amenity_data),
                          content_type='application/json')
    
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        created_amenity = response.get_json()
        print(f"   ✅ Amenity created: {created_amenity['name']}")
        amenity_id = created_amenity['id']
    else:
        print(f"   ❌ Failed: {response.get_json()}")
        amenity_id = None
    
    # Test 2: Create another amenity
    print("\n2. Creating second amenity...")
    response = client.post('/api/v1/amenities/', 
                          data=json.dumps({'name': 'Air Conditioning'}),
                          content_type='application/json')
    
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        print(f"   ✅ Second amenity created")
    
    # Test 3: Get all amenities
    print("\n3. Testing GET /api/v1/amenities/ - Get all amenities")
    response = client.get('/api/v1/amenities/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        amenities = response.get_json()
        print(f"   ✅ Retrieved {len(amenities)} amenity(ies)")
        for amenity in amenities:
            print(f"     - {amenity['name']}")
    else:
        print(f"   ❌ Failed: {response.get_json()}")
    
    # Test 4: Get amenity by ID
    if amenity_id:
        print(f"\n4. Testing GET /api/v1/amenities/{amenity_id} - Get amenity by ID")
        response = client.get(f'/api/v1/amenities/{amenity_id}')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            amenity = response.get_json()
            print(f"   ✅ Retrieved amenity: {amenity['name']}")
        else:
            print(f"   ❌ Failed: {response.get_json()}")
    
    # Test 5: Update amenity
    if amenity_id:
        print(f"\n5. Testing PUT /api/v1/amenities/{amenity_id} - Update amenity")
        update_data = {
            'name': 'High-Speed Wi-Fi'
        }
        
        response = client.put(f'/api/v1/amenities/{amenity_id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            updated_amenity = response.get_json()
            print(f"   ✅ Amenity updated: {updated_amenity['name']}")
        else:
            print(f"   ❌ Failed: {response.get_json()}")
    
    # Test 6: Get non-existent amenity
    print("\n6. Testing GET /api/v1/amenities/nonexistent - Get non-existent amenity")
    response = client.get('/api/v1/amenities/nonexistent')
    print(f"   Status: {response.status_code}")
    if response.status_code == 404:
        print(f"   ✅ Correctly returned 404 for non-existent amenity")
    else:
        print(f"   ❌ Should have returned 404")

print("\n" + "="*50)
print("✅ Task 03 Amenity Endpoints Test Complete!")
print("="*50)
