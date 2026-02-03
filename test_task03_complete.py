#!/usr/bin/env python3
"""Complete test for Task 03 requirements."""
import json
import sys

print("="*60)
print("TASK 03: AMENITY ENDPOINTS COMPREHENSIVE TEST")
print("="*60)

from app import create_app
app = create_app()

test_results = []

def run_test(name, test_func):
    """Run a test and record results."""
    try:
        result = test_func()
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
    created_amenities = []
    
    # Test 1: Create amenity
    def test_create_amenity():
        resp = client.post('/api/v1/amenities/', 
                          data=json.dumps({'name': 'Swimming Pool'}),
                          content_type='application/json')
        assert resp.status_code == 201, f"Expected 201, got {resp.status_code}"
        amenity = resp.get_json()
        assert 'id' in amenity
        assert amenity['name'] == 'Swimming Pool'
        created_amenities.append(amenity)
        return amenity
    
    amenity1 = run_test("1. POST /api/v1/amenities/ - Create amenity", test_create_amenity)
    
    # Test 2: Create another amenity
    def test_create_second_amenity():
        resp = client.post('/api/v1/amenities/', 
                          data=json.dumps({'name': 'Gym'}),
                          content_type='application/json')
        assert resp.status_code == 201
        amenity = resp.get_json()
        created_amenities.append(amenity)
        return amenity
    
    amenity2 = run_test("2. POST /api/v1/amenities/ - Create second amenity", test_create_second_amenity)
    
    # Test 3: Get all amenities
    def test_get_all_amenities():
        resp = client.get('/api/v1/amenities/')
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        amenities = resp.get_json()
        assert isinstance(amenities, list)
        assert len(amenities) >= 2
        
        # Check that our amenities are in the list
        amenity_ids = [a['id'] for a in amenities]
        assert amenity1['id'] in amenity_ids
        assert amenity2['id'] in amenity_ids
        
        return amenities
    
    all_amenities = run_test("3. GET /api/v1/amenities/ - Get all amenities", test_get_all_amenities)
    
    # Test 4: Get amenity by ID
    def test_get_amenity_by_id():
        resp = client.get(f'/api/v1/amenities/{amenity1["id"]}')
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        amenity = resp.get_json()
        assert amenity['id'] == amenity1['id']
        assert amenity['name'] == 'Swimming Pool'
    
    run_test("4. GET /api/v1/amenities/<id> - Get amenity by ID", test_get_amenity_by_id)
    
    # Test 5: Update amenity
    def test_update_amenity():
        resp = client.put(f'/api/v1/amenities/{amenity1["id"]}',
                         data=json.dumps({'name': 'Olympic Swimming Pool'}),
                         content_type='application/json')
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        updated = resp.get_json()
        assert updated['name'] == 'Olympic Swimming Pool'
        
        # Verify the update persisted
        resp = client.get(f'/api/v1/amenities/{amenity1["id"]}')
        assert resp.status_code == 200
        verified = resp.get_json()
        assert verified['name'] == 'Olympic Swimming Pool'
        
        return updated
    
    run_test("5. PUT /api/v1/amenities/<id> - Update amenity", test_update_amenity)
    
    # Test 6: Get non-existent amenity
    def test_nonexistent_amenity():
        resp = client.get('/api/v1/amenities/nonexistent-id-12345')
        assert resp.status_code == 404, f"Expected 404, got {resp.status_code}"
        error = resp.get_json()
        assert 'error' in error
    
    run_test("6. GET /api/v1/amenities/<id> - Non-existent amenity", test_nonexistent_amenity)
    
    # Test 7: Update non-existent amenity
    def test_update_nonexistent_amenity():
        resp = client.put('/api/v1/amenities/nonexistent-id-12345',
                         data=json.dumps({'name': 'Test'}),
                         content_type='application/json')
        assert resp.status_code == 404, f"Expected 404, got {resp.status_code}"
    
    run_test("7. PUT /api/v1/amenities/<id> - Update non-existent amenity", test_update_nonexistent_amenity)

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
    print("\n🎉 TASK 03 COMPLETE! All amenity endpoints implemented correctly.")
    print("You can now proceed to Task 04 (Place)")
else:
    print(f"\n⚠️ {total - passed} test(s) failed. Please fix the issues.")
    print("Check the error messages above for details.")

print("="*60)
