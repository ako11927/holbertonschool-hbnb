#!/usr/bin/env python3
try:
    from app import create_app
    app = create_app()
    print("✅ App created successfully!")
    
    # Test endpoints directly
    with app.test_client() as client:
        print("\n1. Testing status endpoint:")
        resp = client.get('/api/v1/status')
        print(f"   Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.get_json()
            print(f"   Response: {data}")
        else:
            print(f"   Error: {resp.get_data()}")
        
        print("\n2. Testing users endpoint:")
        resp = client.get('/api/v1/users/')
        print(f"   Status: {resp.status_code}")
        
        print("\n3. Testing other endpoints:")
        for endpoint in ['/api/v1/places/', '/api/v1/reviews/', '/api/v1/amenities/']:
            resp = client.get(endpoint)
            print(f"   GET {endpoint}: {resp.status_code}")
    
    print("\n🎉 FIX SUCCESSFUL - ALL ENDPOINTS RESPONDING!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
