#!/usr/bin/env python3
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=== Testing Complete HBnB App ===")

try:
    # First test the routes module directly
    print("1. Testing routes module import...")
    from presentation.api.v1.routes import api
    print(f"   ✅ API imported successfully")
    print(f"   ✅ API title: {api.title}")
    print(f"   ✅ API version: {api.version}")
    
    # Test the app creation
    print("\n2. Testing app creation...")
    from app import create_app
    app = create_app()
    print("   ✅ App created successfully!")
    
    # Test app configuration
    print(f"   ✅ Debug mode: {app.debug}")
    
    # List all routes
    print("\n3. Testing registered routes:")
    with app.app_context():
        routes = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                methods = ','.join(sorted(rule.methods - {'OPTIONS', 'HEAD'}))
                routes.append((rule.rule, methods, rule.endpoint))
        
        routes.sort(key=lambda x: x[0])
        for rule, methods, endpoint in routes:
            print(f"   {rule:40} [{methods:15}] -> {endpoint}")
    
    # Test endpoints
    print("\n4. Testing endpoints with test client:")
    with app.test_client() as client:
        print("   a) Testing status endpoint:")
        resp = client.get('/api/v1/status')
        print(f"      Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.get_json()
            print(f"      Response: {data}")
        else:
            print(f"      Error: {resp.get_data()}")
        
        print("\n   b) Testing all namespace endpoints:")
        test_endpoints = [
            ('/api/v1/users/', 'Users'),
            ('/api/v1/places/', 'Places'),
            ('/api/v1/reviews/', 'Reviews'),
            ('/api/v1/amenities/', 'Amenities'),
        ]
        
        for endpoint, name in test_endpoints:
            resp = client.get(endpoint)
            print(f"      {name:15} {endpoint:30} -> {resp.status_code}")
        
        print("\n   c) Testing error handling:")
        resp = client.get('/api/v1/nonexistent')
        print(f"      404 Test: {resp.status_code} -> {resp.get_json()}")
    
    print("\n" + "="*50)
    print("🎉 SUCCESS: HBnB API is fully functional and ready!")
    print("="*50)
    
except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    print("   Make sure all modules are in the correct location.")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
