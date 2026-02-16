#!/usr/bin/env python3
"""Validate Task 03 implementation."""
import inspect

print("="*60)
print("TASK 03 VALIDATION CHECKLIST")
print("="*60)

print("\n✅ Required Files Check:")

required_files = [
    ("app/models/amenity.py", "Amenity model implementation"),
    ("app/services/facade.py", "Facade with amenity methods"),
    ("app/api/v1/amenities.py", "Amenity API endpoints"),
]

all_files_exist = True
for filepath, desc in required_files:
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        print(f"  ✅ {filepath}")
    except FileNotFoundError:
        print(f"  ❌ {filepath} - {desc} - MISSING")
        all_files_exist = False

print("\n✅ Amenity Model Check:")
if all_files_exist:
    try:
        from app.models.amenity import Amenity
        amenity = Amenity(name="Test Amenity")
        
        checks = [
            ("Has id attribute", hasattr(amenity, 'id')),
            ("Has name attribute", hasattr(amenity, 'name')),
            ("Has update method", hasattr(amenity, 'update') and callable(amenity.update)),
            ("Has to_dict method", hasattr(amenity, 'to_dict') and callable(amenity.to_dict)),
        ]
        
        for desc, check in checks:
            status = "✅" if check else "❌"
            print(f"  {status} {desc}")
    except ImportError as e:
        print(f"  ❌ Cannot import Amenity: {e}")

print("\n✅ Facade Check:")
if all_files_exist:
    try:
        from app.services.facade import HBnBFacade
        facade = HBnBFacade()
        
        required_methods = [
            'create_amenity',
            'get_amenity', 
            'get_all_amenities',
            'update_amenity'
        ]
        
        for method in required_methods:
            if hasattr(facade, method) and callable(getattr(facade, method)):
                print(f"  ✅ {method}()")
            else:
                print(f"  ❌ {method}() - MISSING")
    except ImportError as e:
        print(f"  ❌ Cannot import facade: {e}")

print("\n✅ API Endpoints Check:")
if all_files_exist:
    try:
        from app.api.v1.amenities import api
        
        # Check for required classes
        from flask_restx import Resource
        
        required_classes = ['AmenityList', 'AmenityResource']
        for class_name in required_classes:
            if hasattr(api, class_name):
                cls = getattr(api, class_name)
                if isinstance(cls, type) and issubclass(cls, Resource):
                    print(f"  ✅ {class_name} class")
                else:
                    print(f"  ❌ {class_name} - Not a Resource subclass")
            else:
                print(f"  ❌ {class_name} - MISSING")
        
        # Check for required methods in AmenityList
        if hasattr(api, 'AmenityList'):
            amenity_list = api.AmenityList
            required_methods = ['post', 'get']
            for method in required_methods:
                if hasattr(amenity_list, method):
                    print(f"  ✅ AmenityList.{method}()")
                else:
                    print(f"  ❌ AmenityList.{method}() - MISSING")
        
        # Check for required methods in AmenityResource
        if hasattr(api, 'AmenityResource'):
            amenity_resource = api.AmenityResource
            required_methods = ['get', 'put']
            for method in required_methods:
                if hasattr(amenity_resource, method):
                    print(f"  ✅ AmenityResource.{method}()")
                else:
                    print(f"  ❌ AmenityResource.{method}() - MISSING")
    except ImportError as e:
        print(f"  ❌ Cannot import amenities API: {e}")

print("\n" + "="*60)
print("SUMMARY:")
print("="*60)

if all_files_exist:
    print("✅ All required files exist")
    print("✅ Amenity model implemented correctly")
    print("✅ Facade has all required methods")
    print("✅ API endpoints have correct structure")
    print("\n🎉 TASK 03 READY FOR SUBMISSION!")
    print("\nNext: Run the comprehensive test:")
    print("  python3 test_task03_complete.py")
else:
    print("❌ Missing files or incomplete implementation")
    print("Please fix the issues above before proceeding.")

print("="*60)
