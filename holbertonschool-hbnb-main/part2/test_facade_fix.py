#!/usr/bin/env python3
import json
from app import create_app
from app.services.facade import HBnBFacade

print("=== Testing Facade ===")

# Test facade directly
facade = HBnBFacade()
print("1. Testing facade methods...")

# Check if methods exist
methods = ['create_user', 'get_user', 'get_all_users', 'get_user_by_email', 'update_user']
for method in methods:
    if hasattr(facade, method):
        print(f"   ✅ {method} exists")
    else:
        print(f"   ❌ {method} missing")

# Test creating a user
print("\n2. Testing user creation...")
user_data = {'first_name': 'Test', 'last_name': 'User', 'email': 'test@example.com'}
user = facade.create_user(user_data)
print(f"   ✅ User created: {user.id}")

# Test get_user_by_email
print("\n3. Testing get_user_by_email...")
found_user = facade.get_user_by_email('test@example.com')
if found_user and found_user.id == user.id:
    print(f"   ✅ Found user by email")
else:
    print(f"   ❌ Could not find user by email")

# Test with Flask app
print("\n4. Testing with Flask app...")
app = create_app()

with app.test_client() as client:
    resp = client.post('/api/v1/users/', 
                      data=json.dumps({
                          'first_name': 'John',
                          'last_name': 'Doe',
                          'email': 'john@example.com'
                      }),
                      content_type='application/json')
    
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 201:
        print(f"   ✅ User created via API")
    else:
        print(f"   ❌ API error: {resp.get_json()}")
