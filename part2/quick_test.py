#!/usr/bin/env python3
import json
from app import create_app

app = create_app()
print("✅ App created")

with app.test_client() as client:
    print("\n1. Testing status endpoint...")
    resp = client.get('/api/v1/status')
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        print(f"   Response: {resp.get_json()}")
    
    print("\n2. Creating a user...")
    resp = client.post('/api/v1/users/', 
                      data=json.dumps({
                          'first_name': 'Test',
                          'last_name': 'User',
                          'email': 'test@example.com'
                      }),
                      content_type='application/json')
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 201:
        user = resp.get_json()
        print(f"   ✅ User created: {user['first_name']}")
        
        print(f"\n3. Getting user by ID...")
        resp = client.get(f"/api/v1/users/{user['id']}")
        print(f"   Status: {resp.status_code}")
        if resp.status_code == 200:
            print(f"   ✅ User retrieved")
    
    print("\n4. Getting all users...")
    resp = client.get('/api/v1/users/')
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        users = resp.get_json()
        print(f"   ✅ Retrieved {len(users)} user(s)")

print("\n🎉 Task 02 endpoints are working!")
