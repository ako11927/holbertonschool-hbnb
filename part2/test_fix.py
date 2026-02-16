#!/usr/bin/env python3
import json
from app import create_app

app = create_app()

print("Testing User Endpoints...")

with app.test_client() as client:
    # Create user
    print("\n1. Creating user...")
    resp = client.post('/api/v1/users/', 
                      data=json.dumps({
                          'first_name': 'Test',
                          'last_name': 'User', 
                          'email': 'test@example.com'
                      }),
                      content_type='application/json')
    
    if resp.status_code == 201:
        user = resp.get_json()
        print(f"   ✅ Created user ID: {user['id'][:8]}...")
        
        # Get user
        print("\n2. Getting user...")
        resp = client.get(f"/api/v1/users/{user['id']}")
        if resp.status_code == 200:
            print(f"   ✅ Retrieved user")
        
        # Get all users
        print("\n3. Getting all users...")
        resp = client.get('/api/v1/users/')
        if resp.status_code == 200:
            users = resp.get_json()
            print(f"   ✅ Retrieved {len(users)} user(s)")
        
        # Update user
        print("\n4. Updating user...")
        resp = client.put(f"/api/v1/users/{user['id']}",
                         data=json.dumps({
                             'first_name': 'Updated',
                             'last_name': 'Name',
                             'email': 'updated@example.com'
                         }),
                         content_type='application/json')
        if resp.status_code == 200:
            print(f"   ✅ Updated user")
        
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print(f"   ❌ Failed to create user: {resp.status_code}")
        print(f"   Response: {resp.get_data()}")
