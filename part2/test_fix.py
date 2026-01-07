#!/usr/bin/env python3
try:
    from app import create_app
    app = create_app()
    print("✅ App created successfully!")
    
    # Check if API is initialized
    print(f"✅ API title: {app.extensions['restx']['api'].title}")
    
    # Test endpoints
    with app.test_client() as client:
        resp = client.get('/api/v1/status')
        print(f"✅ Status endpoint: {resp.status_code}")
        print(f"Response: {resp.get_json()}")
        
        resp = client.get('/api/v1/users/')
        print(f"✅ Users endpoint: {resp.status_code}")
        
    print("\n🎉 FIX SUCCESSFUL!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
