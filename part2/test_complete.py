#!/usr/bin/env python3
"""Complete test for Place and Review endpoints"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_models_exist():
    """Check if all model files exist"""
    print("=" * 60)
    print("Checking Model Files")
    print("=" * 60)
    
    model_files = ['models/user.py', 'models/place.py', 'models/amenity.py', 'models/review.py']
    
    for file in model_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
            # Try to import it
            try:
                if file == 'models/user.py':
                    from models.user import User
                    print(f"  Can import User class")
                elif file == 'models/place.py':
                    from models.place import Place
                    print(f"  Can import Place class")
                elif file == 'models/amenity.py':
                    from models.amenity import Amenity
                    print(f"  Can import Amenity class")
                elif file == 'models/review.py':
                    from models.review import Review
                    print(f"  Can import Review class")
            except Exception as e:
                print(f"  ✗ Error importing: {e}")
        else:
            print(f"✗ {file} does not exist")

def test_facade():
    """Test the facade"""
    print("\n" + "=" * 60)
    print("Testing Facade")
    print("=" * 60)
    
    try:
        from services.facade import facade
        
        print(f"✓ Facade instance created")
        print(f"  Type: {type(facade)}")
        
        # Check attributes
        print(f"\nChecking facade attributes:")
        print(f"  has 'users': {hasattr(facade, 'users')}")
        print(f"  has 'places': {hasattr(facade, 'places')}")
        print(f"  has 'amenities': {hasattr(facade, 'amenities')}")
        print(f"  has 'reviews': {hasattr(facade, 'reviews')}")
        
        if hasattr(facade, 'users'):
            print(f"\nData loaded:")
            print(f"  Users: {len(facade.users)}")
            print(f"  Places: {len(facade.places)}")
            print(f"  Amenities: {len(facade.amenities)}")
            print(f"  Reviews: {len(facade.reviews)}")
            
            # Show sample data
            if facade.users:
                print(f"\nSample user: {list(facade.users.values())[0].first_name} {list(facade.users.values())[0].last_name}")
            if facade.places:
                print(f"Sample place: {list(facade.places.values())[0].title}")
        
        # Test methods
        print(f"\nTesting facade methods:")
        print(f"  has 'create_place': {hasattr(facade, 'create_place')}")
        print(f"  has 'get_place': {hasattr(facade, 'get_place')}")
        print(f"  has 'get_all_places': {hasattr(facade, 'get_all_places')}")
        print(f"  has 'create_review': {hasattr(facade, 'create_review')}")
        
    except Exception as e:
        print(f"✗ Error testing facade: {e}")
        import traceback
        traceback.print_exc()

def test_api_endpoints():
    """Test API endpoint imports"""
    print("\n" + "=" * 60)
    print("Testing API Endpoints")
    print("=" * 60)
    
    api_files = ['api/v1/places.py', 'api/v1/reviews.py']
    
    for file in api_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} does not exist")
    
    # Try to import from app
    try:
        from app import create_app
        print(f"\n✓ Can import create_app from app")
        
        # Try to create app
        app = create_app()
        print(f"✓ Can create app instance")
        
        # Check if API blueprint is registered
        blueprints = [bp.name for bp in app.blueprints.values()]
        print(f"  Registered blueprints: {blueprints}")
        
    except Exception as e:
        print(f"\n✗ Error with app: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("Starting comprehensive test...")
    test_models_exist()
    test_facade()
    test_api_endpoints()
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)
