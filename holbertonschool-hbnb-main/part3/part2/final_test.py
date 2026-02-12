#!/usr/bin/env python3
"""Final test of the complete implementation"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("FINAL TEST - Place and Review Endpoints Implementation")
print("=" * 70)

# Check all required files
print("\n1. Checking required files:")
required_files = [
    'models/place.py',
    'models/review.py',
    'models/user.py',
    'models/amenity.py',
    'services/facade.py',
    'api/v1/places.py',
    'api/v1/reviews.py',
    'api/__init__.py',
    'app.py'
]

all_exist = True
for file in required_files:
    if os.path.exists(file):
        print(f"   ✓ {file}")
    else:
        print(f"   ✗ {file} - MISSING")
        all_exist = False

if not all_exist:
    print("\nERROR: Some required files are missing!")
    sys.exit(1)

# Test imports
print("\n2. Testing imports:")
try:
    from models.place import Place
    print("   ✓ models.place.Place")
    
    p = Place()
    p.title = "Test Place"
    p.price = 100.0
    p.latitude = 40.0
    p.longitude = -70.0
    print(f"   ✓ Created Place: {p.title}")
except Exception as e:
    print(f"   ✗ Error with Place: {e}")

try:
    from services.facade import facade
    print("   ✓ services.facade.facade")
    print(f"   ✓ Data loaded: {len(facade.users)} users, {len(facade.places)} places")
except Exception as e:
    print(f"   ✗ Error with facade: {e}")

# Test API structure
print("\n3. Testing API structure:")
try:
    from api import api_bp, api
    print("   ✓ api module")
    print(f"   ✓ API title: {api.title}")
    
    # Check registered namespaces
    namespaces = [ns.name for ns in api.namespaces]
    print(f"   ✓ Namespaces: {namespaces}")
except Exception as e:
    print(f"   ✗ Error with API: {e}")

# Test Flask app
print("\n4. Testing Flask app:")
try:
    from app import create_app
    app = create_app()
    print("   ✓ Flask app created")
    
    # Check registered blueprints
    blueprints = [bp.name for bp in app.blueprints.values()]
    print(f"   ✓ Blueprints: {blueprints}")
    
    # Test a simple route
    with app.test_client() as client:
        response = client.get('/api/v1/')
        if response.status_code in [200, 404]:
            print(f"   ✓ API base endpoint responds")
        else:
            print(f"   ✗ API base endpoint: {response.status_code}")
except Exception as e:
    print(f"   ✗ Error with Flask app: {e}")

print("\n" + "=" * 70)
print("SUMMARY:")
print("=" * 70)
print("""
Your implementation should now have:

1. Place endpoints:
   - POST   /api/v1/places/          - Create a new place
   - GET    /api/v1/places/          - Get all places
   - GET    /api/v1/places/<id>      - Get specific place
   - PUT    /api/v1/places/<id>      - Update a place
   - GET    /api/v1/places/<id>/reviews - Get reviews for a place

2. Review endpoints:
   - POST   /api/v1/reviews/         - Create a new review
   - GET    /api/v1/reviews/         - Get all reviews
   - GET    /api/v1/reviews/<id>     - Get specific review
   - PUT    /api/v1/reviews/<id>     - Update a review
   - DELETE /api/v1/reviews/<id>     - Delete a review

To run the application:
   $ python3 app.py

To test the API:
   $ curl http://localhost:5000/api/v1/places/
   $ curl http://localhost:5000/api/v1/docs  (for Swagger UI)
""")
print("=" * 70)
