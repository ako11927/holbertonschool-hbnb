#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")
try:
    from models.place import Place
    print("✓ Imported Place")
    p = Place()
    print(f"  Created place with ID: {p.id}")
except Exception as e:
    print(f"✗ Error importing Place: {e}")

try:
    from services.facade import facade
    print("✓ Imported facade")
    print(f"  Facade has users: {hasattr(facade, 'users')}")
    if hasattr(facade, 'users'):
        print(f"  Number of users: {len(facade.users)}")
except Exception as e:
    print(f"✗ Error importing facade: {e}")
