#!/usr/bin/env python3
"""Final comprehensive test for Task 02."""
import json
import sys
from app import create_app

print("="*60)
print("TASK 02 FINAL VALIDATION TEST")
print("="*60)

app = create_app()
test_results = []

def test(name, func):
    """Run a test and record result."""
    try:
        result = func()
        test_results.append((name, True, result))
        print(f"✅ {name}")
        return result
    except AssertionError as e:
        test_results.append((name, False, str(e)))
        print(f"❌ {name}: {e}")
        return None
    except Exception as e:
        test_results.append((name, False, str(e)))
        print(f"❌ {name}: {e}")
        return None

with app.test_client() as client:
    created_users = []
    
    # Test 1: Create user
    user1 = test("1. Create user (POST /api/v1/users/)", lambda: (
        resp = client.post('/api/v1/users/', 
                          data=json.dumps({
                              'first_name': 'Alice',
                              'last_name': 'Johnson',
                              'email': 'alice@example.com'
                          }),
                          content_type='application/json'),
        assert resp.status_code == 201, f"Expected 201, got {resp.status_code}",
        user = resp.get_json(),
        assert 'id' in user,
        assert user['first_name'] == 'Alice',
        assert user['last_name'] == 'Johnson',
        assert user['email'] == 'alice@example.com',
        created_users.append(user),
        user
    ))
    
    # Test 2: Duplicate email
    test("2. Reject duplicate email", lambda: (
        resp = client.post('/api/v1/users/', 
                          data=json.dumps({
                              'first_name': 'Bob',
                              'last_name': 'Duplicate',
                              'email': 'alice@example.com'  # Same as user1
                          }),
                          content_type='application/json'),
        assert resp.status_code == 400, f"Expected 400, got {resp.status_code}",
        error = resp.get_json(),
        assert 'error' in error,
        assert 'already registered' in error['error'].lower()
    ))
    
    # Test 3: Create second user
    user2 = test("3. Create second user", lambda: (
        resp = client.post('/api/v1/users/', 
                          data=json.dumps({
                              'first_name': 'Bob',
                              'last_name': 'Smith',
                              'email': 'bob@example.com'
                          }),
                          content_type='application/json'),
        assert resp.status_code == 201,
        user = resp.get_json(),
        created_users.append(user),
        user
    ))
    
    # Test 4: Get all users
    test("4. Get all users (GET /api/v1/users/)", lambda: (
        resp = client.get('/api/v1/users/'),
        assert resp.status_code == 200,
        users = resp.get_json(),
        assert isinstance(users, list),
        assert len(users) >= 2
    ))
    
    # Test 5: Get user by ID
    if user1:
        test("5. Get user by ID", lambda: (
            resp = client.get(f'/api/v1/users/{user1["id"]}'),
            assert resp.status_code == 200,
            user = resp.get_json(),
            assert user['id'] == user1['id'],
            assert user['first_name'] == 'Alice'
        ))
    
    # Test 6: Update user
    if user1:
        test("6. Update user (PUT /api/v1/users/<id>)", lambda: (
            resp = client.put(f'/api/v1/users/{user1["id"]}',
                            data=json.dumps({
                                'first_name': 'Alicia',
                                'last_name': 'Johnson-Updated',
                                'email': 'alicia.updated@example.com'
                            }),
                            content_type='application/json'),
            assert resp.status_code == 200,
            updated = resp.get_json(),
            assert updated['first_name'] == 'Alicia',
            assert updated['email'] == 'alicia.updated@example.com'
        ))
    
    # Test 7: Update with duplicate email (should fail)
    if user1 and user2:
        test("7. Reject update with duplicate email", lambda: (
            resp = client.put(f'/api/v1/users/{user1["id"]}',
                            data=json.dumps({
                                'first_name': 'Alice',
                                'last_name': 'Johnson',
                                'email': user2['email']  # user2's email
                            }),
                            content_type='application/json'),
            assert resp.status_code == 400,
            error = resp.get_json(),
            assert 'error' in error
        ))
    
    # Test 8: Get non-existent user
    test("8. Get non-existent user returns 404", lambda: (
        resp = client.get('/api/v1/users/nonexistent-12345'),
        assert resp.status_code == 404,
        error = resp.get_json(),
        assert 'error' in error
    ))

# Summary
print("\n" + "="*60)
print("TEST SUMMARY")
print("="*60)

passed = sum(1 for _, success, _ in test_results if success)
total = len(test_results)

for name, success, _ in test_results:
    status = "✅" if success else "❌"
    print(f"{status} {name}")

print(f"\nTotal: {passed}/{total} tests passed")

if passed == total:
    print("\n🎉 TASK 02 COMPLETED SUCCESSFULLY!")
    print("All user endpoints are working correctly.")
else:
    print(f"\n⚠️ {total - passed} test(s) failed.")

print("="*60)
