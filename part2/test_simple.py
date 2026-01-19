#!/usr/bin/env python3
import json
from app import create_app

app = create_app()

print("=== Simple Test ===")

with app.test_client() as client:
    print("\n1. Test status endpoint from routes.py...")
    resp = client.get('/api/v1/status')
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        print(f"   Response: {resp.get_json()}")
    
    print("\n2. Create a user...")
    resp = client.post('/api/v1/users/', 
                      data=json.dumps({
                          'first_name': 'John',
                          'last_name': 'Doe',
                          'email': 'john@example.com'
                      }),
                      content_type='application/json')
    print(f"   Status: {resp.status_code}")
    
    if resp.status_code == 201:
        user = resp.get_json()
        print(f"   ✅ Created user: {user['first_name']}")
        user_id = user['id']
        
        print(f"\n3. Get user by ID...")
        resp = client.get(f'/api/v1/users/{user_id}')
        print(f"   Status: {resp.status_code}")
        if resp.status_code == 200:
            print(f"   ✅ Retrieved user")
        
        print(f"\n4. Get all users...")
        resp = client.get('/api/v1/users/')
        print(f"   Status: {resp.status_code}")
        if resp.status_code == 200:
            users = resp.get_json()
            print(f"   ✅ Retrieved {len(users)} user(s)")
        
        print(f"\n5. Update user...")
        resp = client.put(f'/api/v1/users/{user_id}',
                         data=json.dumps({
                             'first_name': 'Jane',
                             'last_name': 'Smith',
                             'email': 'jane@example.com'
                         }),
                         content_type='application/json')
        print(f"   Status: {resp.status_code}")
        if resp.status_code == 200:
            print(f"   ✅ Updated user")
    
    print("\n" + "="*50)
    if resp.status_code != 404:
        print("✅ User endpoints are working!")
    else:
        print("❌ Endpoints returning 404 - need to fix")
