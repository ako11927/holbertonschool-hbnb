#!/usr/bin/env python3
"""Test User endpoints for Task 02."""
import json
from app import create_app

app = create_app()

print("=== Testing User Endpoints (Task 02) ===")

with app.test_client() as client:
    # Test 1: Create a user (POST)
    print("\n1. Testing POST /api/v1/users/ - Create user")
    user_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com'
    }
    
    response = client.post('/api/v1/users/', 
                          data=json.dumps(user_data),
                          content_type='application/json')
    
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        created_user = response.get_json()
        print(f"   ✅ User created: {created_user['first_name']} {created_user['last_name']}")
        user_id = created_user['id']
    else:
        print(f"   ❌ Failed: {response.get_json()}")
        user_id = None
    
    # Test 2: Try to create duplicate email
    print("\n2. Testing duplicate email validation")
    response = client.post('/api/v1/users/',
                          data=json.dumps(user_data),
                          content_type='application/json')
    print(f"   Status: {response.status_code}")
    if response.status_code == 400:
        print(f"   ✅ Correctly rejected duplicate email")
    else:
        print(f"   ❌ Should have rejected duplicate")
    
    # Test 3: Get all users
    print("\n3. Testing GET /api/v1/users/ - List all users")
    response = client.get('/api/v1/users/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        users = response.get_json()
        print(f"   ✅ Retrieved {len(users)} user(s)")
        for user in users:
            print(f"     - {user['first_name']} {user['last_name']} ({user['email']})")
    else:
        print(f"   ❌ Failed: {response.get_json()}")
    
    # Test 4: Get user by ID
    if user_id:
        print(f"\n4. Testing GET /api/v1/users/{user_id} - Get user by ID")
        response = client.get(f'/api/v1/users/{user_id}')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            user = response.get_json()
            print(f"   ✅ Retrieved user: {user['first_name']} {user['last_name']}")
        else:
            print(f"   ❌ Failed: {response.get_json()}")
    
    # Test 5: Update user
    if user_id:
        print(f"\n5. Testing PUT /api/v1/users/{user_id} - Update user")
        update_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com'
        }
        
        response = client.put(f'/api/v1/users/{user_id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            updated_user = response.get_json()
            print(f"   ✅ User updated: {updated_user['first_name']} {updated_user['last_name']}")
            print(f"   ✅ New email: {updated_user['email']}")
        else:
            print(f"   ❌ Failed: {response.get_json()}")
    
    # Test 6: Get non-existent user
    print("\n6. Testing GET /api/v1/users/nonexistent - Get non-existent user")
    response = client.get('/api/v1/users/nonexistent')
    print(f"   Status: {response.status_code}")
    if response.status_code == 404:
        print(f"   ✅ Correctly returned 404 for non-existent user")
    else:
        print(f"   ❌ Should have returned 404")
    
    # Test 7: Create second user
    print("\n7. Testing creation of second user")
    user2_data = {
        'first_name': 'Bob',
        'last_name': 'Johnson',
        'email': 'bob.johnson@example.com'
    }
    
    response = client.post('/api/v1/users/',
                          data=json.dumps(user2_data),
                          content_type='application/json')
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        print(f"   ✅ Second user created successfully")
    else:
        print(f"   ❌ Failed: {response.get_json()}")

print("\n" + "="*50)
print("✅ Task 02 User Endpoints Test Complete!")
print("="*50)
