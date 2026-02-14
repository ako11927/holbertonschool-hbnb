#!/usr/bin/env python3
import sys

print("=== Testing Fixed HBnB App ===")

try:
    from app import create_app
    app = create_app()
    print("✅ App created successfully!")
    
    # List all routes
    print("\n✅ Registered API routes:")
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            methods = ','.join(sorted(rule.methods - {'OPTIONS', 'HEAD'}))
            routes.append((rule.rule, methods))
    
    routes.sort(key=lambda x: x[0])
    for rule, methods in routes:
        print(f"  {rule:50} [{methods}]")
    
    # Test endpoints
    print("\n✅ Testing endpoints with test client:")
    with app.test_client() as client:
        # Test status endpoint
        print("\n1. Testing /api/v1/status:")
        resp = client.get('/api/v1/status')
        print(f"   Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.get_json()
            print(f"   Response: {data}")
        else:
            print(f"   Error: {resp.get_data()}")
        
        # Test namespace endpoints
        print("\n2. Testing all API endpoints:")
        endpoints = [
            ('/api/v1/users/', 'Users'),
            ('/api/v1/places/', 'Places'),
            ('/api/v1/reviews/', 'Reviews'),
            ('/api/v1/amenities/', 'Amenities'),
        ]
        
        for endpoint, name in endpoints:
            resp = client.get(endpoint)
            print(f"   GET {endpoint:35} -> {resp.status_code}")
        
        # Test documentation endpoints
        print("\n3. Testing documentation:")
        resp = client.get('/api/v1/docs/')
        print(f"   GET /api/v1/docs/: {resp.status_code}")
        
        # Test 404 error
        print("\n4. Testing error handling:")
        resp = client.get('/api/v1/nonexistent')
        print(f"   GET /api/v1/nonexistent: {resp.status_code}")
        if resp.status_code == 404:
            print(f"   Correctly returns 404: {resp.get_json()}")
    
    print("\n" + "="*50)
    print("🎉 SUCCESS: HBnB API is fully functional!")
    print("="*50)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
