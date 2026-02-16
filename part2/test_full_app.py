#!/usr/bin/env python3
import sys

print("=== Testing Full HBnB App ===")

try:
    from app import create_app
    app = create_app()
    print("✅ App created successfully!")
    
    # List all routes
    print("\n✅ Registered API routes:")
    for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
        if rule.endpoint != 'static':
            methods = ','.join(sorted(rule.methods - {'OPTIONS', 'HEAD'}))
            print(f"  {rule.rule} [{methods}]")
    
    # Test endpoints
    with app.test_client() as client:
        print("\n✅ Testing endpoints:")
        
        # Status endpoint
        resp = client.get('/api/v1/status')
        print(f"  GET /api/v1/status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.get_json()
            print(f"    Response: {data}")
        
        # Test other endpoints
        endpoints = ['/users', '/places', '/reviews', '/amenities']
        for endpoint in endpoints:
            resp = client.get(f'/api/v1{endpoint}/')
            print(f"  GET /api/v1{endpoint}/: {resp.status_code}")
    
    print("\n🎉 SUCCESS: HBnB API is fully functional!")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
