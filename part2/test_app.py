#!/usr/bin/env python3
"""Test the actual HBnB app."""
try:
    from app import create_app
    app = create_app()
    print("✅ App imported and created")
    
    # Check routes
    print("\nRegistered routes:")
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            print(f"  {rule.rule} -> {rule.endpoint}")
    
    # Test with client
    with app.test_client() as client:
        print("\nTesting endpoints:")
        
        # Status
        resp = client.get('/api/v1/status')
        print(f"  /api/v1/status: {resp.status_code} - {resp.get_json()}")
        
        # Users
        resp = client.get('/api/v1/users/')
        print(f"  /api/v1/users/: {resp.status_code}")
        
        # Places
        resp = client.get('/api/v1/places/')
        print(f"  /api/v1/places/: {resp.status_code}")
        
        # Reviews
        resp = client.get('/api/v1/reviews/')
        print(f"  /api/v1/reviews/: {resp.status_code}")
        
        # Amenities
        resp = client.get('/api/v1/amenities/')
        print(f"  /api/v1/amenities/: {resp.status_code}")
    
    print("\n✅ APP IS WORKING!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
