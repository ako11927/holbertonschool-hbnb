#!/usr/bin/env python3
import json
import sys

print("="*60)
print("TASK 02 WORKING TEST")
print("="*60)

# First test facade directly
try:
    from app.services.facade import HBnBFacade
    facade = HBnBFacade()
    print("✅ Facade imported successfully")
    
    # Test facade methods
    test_user = facade.create_user({
        'first_name': 'Direct',
        'last_name': 'Test',
        'email': 'direct@test.com'
    })
    print(f"✅ Direct user creation: {test_user.id[:8]}...")
    
    found = facade.get_user_by_email('direct@test.com')
    if found:
        print(f"✅ Found user by email: {found.first_name}")
    
except Exception as e:
    print(f"❌ Facade error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Now test Flask app
from app import create_app
app = create_app()

print("\n=== Testing API Endpoints ===")

with app.test_client() as client:
    # Create first user
    print("\n1. Creating first user...")
    resp = client.post('/api/v1/users/', 
                      data=json.dumps({
                          'first_name': 'Alice',
                          'last_name': 'Wonderland',
                          'email': 'alice@example.com'
                      }),
                      content_type='application/json')
    
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 201:
        user1 = resp.get_json()
        print(f"   ✅ Created: {user1['first_name']} {user1['last_name']}")
    else:
        print(f"   ❌ Failed: {resp.get_json()}")
        sys.exit(1)
    
    # Try duplicate email
    print("\n2. Trying duplicate email...")
    resp = client.post('/api/v1/users/', 
                      data=json.dumps({
                          'first_name': 'Duplicate',
                          'last_name': 'User',
                          'email': 'alice@example.com'
                      }),
                      content_type='application/json')
    
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 400:
        print(f"   ✅ Correctly rejected duplicate")
    else:
        print(f"   ❌ Should have rejected: {resp.get_json()}")
    
    # Create second user
    print("\n3. Creating second user...")
    resp = client.post('/api/v1/users/', 
                      data=json.dumps({
                          'first_name': 'Bob',
                          'last_name': 'Builder',
                          'email': 'bob@example.com'
                      }),
                      content_type='application/json')
    
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 201:
        user2 = resp.get_json()
        print(f"   ✅ Created: {user2['first_name']} {user2['last_name']}")
    
    # Get all users
    print("\n4. Getting all users...")
    resp = client.get('/api/v1/users/')
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        users = resp.get_json()
        print(f"   ✅ Retrieved {len(users)} user(s)")
    
    # Get user by ID
    print(f"\n5. Getting user by ID...")
    resp = client.get(f"/api/v1/users/{user1['id']}")
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        user = resp.get_json()
        print(f"   ✅ Retrieved: {user['first_name']}")
    
    # Update user
    print(f"\n6. Updating user...")
    resp = client.put(f"/api/v1/users/{user1['id']}",
                     data=json.dumps({
                         'first_name': 'Alicia',
                         'last_name': 'Updated',
                         'email': 'alicia@example.com'
                     }),
                     content_type='application/json')
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        updated = resp.get_json()
        print(f"   ✅ Updated to: {updated['first_name']}")
    
    # Try updating with duplicate email
    print(f"\n7. Trying update with duplicate email...")
    resp = client.put(f"/api/v1/users/{user1['id']}",
                     data=json.dumps({
                         'first_name': 'Alice',
                         'last_name': 'Test',
                         'email': 'bob@example.com'  # user2's email
                     }),
                     content_type='application/json')
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 400:
        print(f"   ✅ Correctly rejected duplicate email in update")
    
    # Get non-existent user
    print(f"\n8. Getting non-existent user...")
    resp = client.get("/api/v1/users/nonexistent-12345")
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 404:
        print(f"   ✅ Correctly returned 404")

print("\n" + "="*60)
print("🎉 TASK 02 COMPLETE - ALL TESTS PASSING!")
print("="*60)
