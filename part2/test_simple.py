#!/usr/bin/env python3
import sys

print("=== Testing Simple Import ===")

try:
    # Test importing routes
    from presentation.api.v1.routes import api
    print("✅ routes.py imports successfully")
    print(f"✅ API title: {api.title}")
    
    # Test importing namespaces
    from presentation.api.v1.user_routes import api as user_ns
    print("✅ user_routes.py imports successfully")
    print(f"✅ User namespace name: {user_ns.name}")
    
    from presentation.api.v1.amenity_routes import api as amenity_ns
    print("✅ amenity_routes.py imports successfully")
    
    from presentation.api.v1.place_routes import api as place_ns
    print("✅ place_routes.py imports successfully")
    
    from presentation.api.v1.review_routes import api as review_ns
    print("✅ review_routes.py imports successfully")
    
    print("\n✅ All imports successful!")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"❌ Other Error: {e}")
    import traceback
    traceback.print_exc()
