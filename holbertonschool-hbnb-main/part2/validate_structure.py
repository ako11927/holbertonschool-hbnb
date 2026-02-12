import os

# Expected files and directories
expected = [
    "app/__init__.py",
    "app/api/__init__.py",
    "app/api/v1/__init__.py",
    "app/api/v1/users.py",
    "app/api/v1/places.py",
    "app/api/v1/reviews.py",
    "app/api/v1/amenities.py",
    "app/models/__init__.py",
    "app/models/user.py",
    "app/models/place.py",
    "app/models/review.py",
    "app/models/amenity.py",
    "app/services/__init__.py",
    "app/services/facade.py",
    "app/persistence/__init__.py",
    "app/persistence/repository.py",
    "run.py",
    "config.py",
    "requirements.txt"
]

print("Checking project structure...")
all_ok = True
for f in expected:
    if not os.path.exists(f):
        print(f"❌ {f} is missing")
        all_ok = False
    else:
        print(f"✅ {f}")

if all_ok:
    print("\n✅ All files and directories are present.")
else:
    print("\n❌ Some files are missing.")
