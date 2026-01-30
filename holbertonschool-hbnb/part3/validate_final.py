#!/usr/bin/env python3
import json
from app import create_app

app = create_app()

print("="*60)
print("FINAL TASK 02 VALIDATION")
print("="*60)

with app.test_client() as client:
    tests_passed = 0
    total_tests = 6
    
    # Test 1: Create user
    print("\n1. POST /api/v1/users/ - Create user")
    resp = client.post('/api/v1/users/', 
                      data=json.dumps({
                          'first_name': 'Alice',
                          'last_name': 'Test',
                          'email': 'alice@test.com'
                      }),
                      content_type='application/json')
    
    if resp.status_code == 201:
        user1 = resp.get_json()
        print(f"   ✅ PASS - Created user: {user1['id'][:8]}...")
        tests_passed += 1
    else:
        print(f"   ❌ FAIL - Status: {resp.status_code}")
    
    # Test 2: Duplicate email
    print("\n2. POST /api/v1/users/ - Duplicate email")
    resp = client.post('/api/v1/users/', 
                      data=json.dumps({
                          'first_name': 'Bob',
                          'last_name': 'Duplicate',
                          'email': 'alice@test.com'  # Same email
                      }),
                      content_type='application/json')
    
    if resp.status_code == 400 and 'already registered' in str(resp.get_json()):
        print(f"   ✅ PASS - Correctly rejected duplicate")
        tests_passed += 1
    else:
        print(f"   ❌ FAIL - Status: {resp.status_code}")
    
    # Test 3: Get all users
    print("\n3. GET /api/v1/users/ - Get all users")
    resp = client.get('/api/v1/users/')
    
    if resp.status_code == 200:
        users = resp.get_json()
        if isinstance(users, list):
            print(f"   ✅ PASS - Retrieved {len(users)} user(s)")
            tests_passed += 1
        else:
            print(f"   ❌ FAIL - Response is not a list")
    else:
        print(f"   ❌ FAIL - Status: {resp.status_code}")
    
    # Test 4: Get user by ID
    if 'user1' in locals():
        print(f"\n4. GET /api/v1/users/<id> - Get user by ID")
        resp = client.get(f"/api/v1/users/{user1['id']}")
        
        if resp.status_code == 200:
            user = resp.get_json()
            if user['id'] == user1['id']:
                print(f"   ✅ PASS - Retrieved correct user")
                tests_passed += 1
            else:
                print(f"   ❌ FAIL - Wrong user retrieved")
        else:
            print(f"   ❌ FAIL - Status: {resp.status_code}")
    
    # Test 5: Update user
    if 'user1' in locals():
        print(f"\n5. PUT /api/v1/users/<id> - Update user")
        resp = client.put(f"/api/v1/users/{user1['id']}",
                         data=json.dumps({
                             'first_name': 'Alicia',
                             'last_name': 'Updated',
                             'email': 'alicia@updated.com'
                         }),
                         content_type='application/json')
        
        if resp.status_code == 200:
            updated = resp.get_json()
            if updated['first_name'] == 'Alicia':
                print(f"   ✅ PASS - User updated successfully")
                tests_passed += 1
            else:
                print(f"   ❌ FAIL - Update didn't work")
        else:
            print(f"   ❌ FAIL - Status: {resp.status_code}")
    
    # Test 6: Get non-existent user
    print(f"\n6. GET /api/v1/users/<id> - Non-existent user")
    resp = client.get("/api/v1/users/nonexistent-12345")
    
    if resp.status_code == 404:
        print(f"   ✅ PASS - Correctly returned 404")
        tests_passed += 1
    else:
        print(f"   ❌ FAIL - Status: {resp.status_code} (expected 404)")

print("\n" + "="*60)
print(f"RESULTS: {tests_passed}/{total_tests} tests passed")
if tests_passed == total_tests:
    print("🎉 TASK 02 COMPLETE AND READY FOR SUBMISSION!")
else:
    print(f"⚠️  {total_tests - tests_passed} test(s) failed")
print("="*60)
