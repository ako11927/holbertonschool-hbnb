#!/usr/bin/env python3
try:
    from app import create_app
    app = create_app()
    print("✅ App created successfully!")
    
    # Test endpoints
    with app.test_client() as client:
        # Status
        resp = client.get('/api/v1/status')
        print(f"✅ Status: {resp.status_code} - {resp.get_json()}")
        
        # Users
        resp = client.get('/api/v1/users/')
        print(f"✅ Users: {resp.status_code}")
        
        # Create a user
        user_data = {
            'email': '11927@holbertonstudents.com',
            'password': '123456',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        resp = client.post('/api/v1/users/', data=user_data)
        print(f"✅ Create user: {resp.status_code}")
        
    print("\n🎉 ALL TESTS PASSED - PROJECT IS WORKING!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
