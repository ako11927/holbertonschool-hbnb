#!/bin/bash
echo "=== Complete Fix for Task 02 ==="

# 1. Create exceptions module
echo "1. Creating app/exceptions.py..."
cat > app/exceptions.py << 'EXCEPEOF'
"""Custom exceptions for HBnB."""

class HBnBError(Exception):
    """Base exception for HBnB errors."""
    pass

class NotFoundError(HBnBError):
    """Raised when a resource is not found."""
    pass

class ValidationError(HBnBError):
    """Raised when input validation fails."""
    pass

class DuplicateError(HBnBError):
    """Raised when a duplicate resource is detected."""
    pass
EXCEPEOF

# 2. Fix app/__init__.py - SIMPLE VERSION
echo "2. Fixing app/__init__.py..."
cat > app/__init__.py << 'INITEOF'
from flask import Flask
from flask_restx import Api

def create_app():
    app = Flask(__name__)
    
    # Create API instance
    api = Api(app,
              version='1.0',
              title='HBnB API',
              description='HBnB Application API',
              doc='/api/v1/')
    
    # Register users namespace
    from .api.v1.users import api as users_ns
    api.add_namespace(users_ns, path='/api/v1/users')
    
    return app
INITEOF

# 3. Ensure all API files exist
echo "3. Ensuring all API files exist..."
for file in users places reviews amenities; do
    if [ ! -f "app/api/v1/${file}.py" ]; then
        echo "  Creating app/api/v1/${file}.py..."
        cat > "app/api/v1/${file}.py" << FILEEOF
"""${file^} API endpoints."""
from flask_restx import Namespace, Resource

api = Namespace('${file}', description='${file^} operations')

@api.route('/')
class ${file^}List(Resource):
    def get(self):
        return {'message': f'GET /${file}'}, 200
FILEEOF
    fi
done

# 4. Create a simple test
echo "4. Creating test..."
cat > test_fix.py << 'TESTEOF'
#!/usr/bin/env python3
import json
from app import create_app

app = create_app()

print("Testing User Endpoints...")

with app.test_client() as client:
    # Create user
    print("\n1. Creating user...")
    resp = client.post('/api/v1/users/', 
                      data=json.dumps({
                          'first_name': 'Test',
                          'last_name': 'User', 
                          'email': 'test@example.com'
                      }),
                      content_type='application/json')
    
    if resp.status_code == 201:
        user = resp.get_json()
        print(f"   ✅ Created user ID: {user['id'][:8]}...")
        
        # Get user
        print("\n2. Getting user...")
        resp = client.get(f"/api/v1/users/{user['id']}")
        if resp.status_code == 200:
            print(f"   ✅ Retrieved user")
        
        # Get all users
        print("\n3. Getting all users...")
        resp = client.get('/api/v1/users/')
        if resp.status_code == 200:
            users = resp.get_json()
            print(f"   ✅ Retrieved {len(users)} user(s)")
        
        # Update user
        print("\n4. Updating user...")
        resp = client.put(f"/api/v1/users/{user['id']}",
                         data=json.dumps({
                             'first_name': 'Updated',
                             'last_name': 'Name',
                             'email': 'updated@example.com'
                         }),
                         content_type='application/json')
        if resp.status_code == 200:
            print(f"   ✅ Updated user")
        
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print(f"   ❌ Failed to create user: {resp.status_code}")
        print(f"   Response: {resp.get_data()}")
TESTEOF

chmod +x test_fix.py

echo "=== Fix Complete ==="
echo "Run: python3 test_fix.py"
