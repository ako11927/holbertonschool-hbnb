import os
import sys

print("=== Task 00 Completion Checklist ===\n")

# Required structure from task instructions
required_structure = {
    "Project Structure": [
        ("app/", "Directory"),
        ("app/__init__.py", "File"),
        ("app/api/", "Directory"),
        ("app/api/__init__.py", "File"),
        ("app/api/v1/", "Directory"),
        ("app/api/v1/__init__.py", "File"),
        ("app/api/v1/users.py", "File"),
        ("app/api/v1/places.py", "File"),
        ("app/api/v1/reviews.py", "File"),
        ("app/api/v1/amenities.py", "File"),
        ("app/models/", "Directory"),
        ("app/models/__init__.py", "File"),
        ("app/models/user.py", "File"),
        ("app/models/place.py", "File"),
        ("app/models/review.py", "File"),
        ("app/models/amenity.py", "File"),
        ("app/services/", "Directory"),
        ("app/services/__init__.py", "File"),
        ("app/services/facade.py", "File"),
        ("app/persistence/", "Directory"),
        ("app/persistence/__init__.py", "File"),
        ("app/persistence/repository.py", "File"),
    ],
    "Root Files": [
        ("run.py", "Application entry point"),
        ("config.py", "Configuration file"),
        ("requirements.txt", "Dependencies"),
        ("README.md", "Documentation"),
    ]
}

all_passed = True

for category, items in required_structure.items():
    print(f"{category}:")
    for path, description in items:
        exists = os.path.exists(path)
        status = "✅" if exists else "❌"
        print(f"  {status} {path:35} - {description}")
        if not exists:
            all_passed = False
    print()

# Check content of key files
print("=== Key File Content Checks ===")
key_files = [
    ("app/__init__.py", "create_app function", "def create_app()"),
    ("app/persistence/repository.py", "Repository classes", "class Repository"),
    ("app/services/facade.py", "HBnBFacade class", "class HBnBFacade"),
    ("run.py", "run.py entry point", "from app import create_app"),
]

for filepath, description, expected_content in key_files:
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            if expected_content in content:
                print(f"✅ {filepath:35} - {description}")
            else:
                print(f"⚠️ {filepath:35} - {description} (content mismatch)")
                all_passed = False
        except:
            print(f"❌ {filepath:35} - Cannot read file")
            all_passed = False
    else:
        print(f"❌ {filepath:35} - File missing")
        all_passed = False

print("\n" + "="*50)
if all_passed:
    print("🎉 TASK 00 COMPLETE! All requirements met.")
    print("You can now proceed to Task 01: Business Logic Layer")
else:
    print("⚠️ Some requirements are not met. Please fix the issues above.")
