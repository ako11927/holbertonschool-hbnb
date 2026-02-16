#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing model imports...")

# Test direct imports
try:
    from models.user import User
    print("✓ Imported User")
    u = User(first_name="Test", last_name="User", email="test@example.com")
    print(f"  Created: {u.first_name} {u.last_name}")
except Exception as e:
    print(f"✗ User import failed: {e}")

try:
    from models.place import Place
    print("✓ Imported Place")
    p = Place(title="Test Place", price=100.0, latitude=40.0, longitude=-70.0)
    print(f"  Created: {p.title} (${p.price})")
except Exception as e:
    print(f"✗ Place import failed: {e}")

try:
    from models.amenity import Amenity
    print("✓ Imported Amenity")
    a = Amenity(name="Wi-Fi")
    print(f"  Created: {a.name}")
except Exception as e:
    print(f"✗ Amenity import failed: {e}")

try:
    from models.review import Review
    print("✓ Imported Review")
    r = Review(text="Great!", rating=5)
    print(f"  Created: review with rating {r.rating}")
except Exception as e:
    print(f"✗ Review import failed: {e}")

# Test package import
print("\nTesting package import...")
try:
    from models import User, Place, Amenity, Review
    print("✓ Imported all from models package")
except Exception as e:
    print(f"✗ Package import failed: {e}")
