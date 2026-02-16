#!/bin/bash
echo "=== Restructuring Project to Match Requirements ==="

# Backup current structure
echo "1. Creating backup..."
mkdir -p backup
cp -r app/ backup/app_backup/ 2>/dev/null || true
cp -r presentation/ backup/presentation_backup/ 2>/dev/null || true
cp -r business_logic/ backup/business_logic_backup/ 2>/dev/null || true

# Clean and create required structure
echo "2. Creating new app structure..."
rm -rf app 2>/dev/null
mkdir -p app/{api/v1,models,services,persistence}

# Create __init__.py files
touch app/__init__.py
touch app/api/__init__.py
touch app/api/v1/__init__.py
touch app/models/__init__.py
touch app/services/__init__.py
touch app/persistence/__init__.py

# Step 1: Create app/__init__.py with Flask app factory
echo "3. Creating app/__init__.py..."
cat > app/__init__.py << 'INIT_EOF'
from flask import Flask
from flask_restx import Api

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Placeholder for API namespaces (endpoints will be added later)
    # Additional namespaces for places, reviews, and amenities will be added later

    return app
INIT_EOF

# Step 2: Move API files if they exist
echo "4. Moving API files..."
if [ -d "presentation/api/v1" ]; then
    cp presentation/api/v1/*.py app/api/v1/ 2>/dev/null || true
    
    # Rename files to match requirements
    cd app/api/v1
    [ -f "user_routes.py" ] && mv user_routes.py users.py
    [ -f "place_routes.py" ] && mv place_routes.py places.py
    [ -f "review_routes.py" ] && mv review_routes.py reviews.py
    [ -f "amenity_routes.py" ] && mv amenity_routes.py amenities.py
    cd ../../..
fi

# Step 3: Move model files if they exist
echo "5. Moving model files..."
if [ -d "business_logic/models" ]; then
    cp business_logic/models/*.py app/models/ 2>/dev/null || true
fi

# Step 4: Create routes.py if it doesn't exist
echo "6. Creating routes.py..."
if [ ! -f "app/api/v1/routes.py" ]; then
    cat > app/api/v1/routes.py << 'ROUTES_EOF'
"""API v1 routes configuration."""
from flask import Blueprint
from flask_restx import Api, Resource

# Create a blueprint for API v1
blueprint = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# Create main API instance attached to the blueprint
api = Api(
    blueprint,
    version='1.0',
    title='HBnB API',
    description='HBnB API operations',
    doc='/docs'
)

# Import namespaces
try:
    from .users import api as user_ns
    from .places import api as place_ns
    from .reviews import api as review_ns
    from .amenities import api as amenity_ns
    
    # Add all namespaces to the main API
    api.add_namespace(user_ns, path='/users')
    api.add_namespace(place_ns, path='/places')
    api.add_namespace(review_ns, path='/reviews')
    api.add_namespace(amenity_ns, path='/amenities')
except ImportError:
    # Placeholder if namespaces aren't ready yet
    pass

# Status endpoint
@api.route('/status')
class Status(Resource):
    """API status endpoint."""
    def get(self):
        return {'status': 'OK', 'version': '1.0'}
ROUTES_EOF
fi

# Step 5: Update app/__init__.py to use routes blueprint
echo "7. Updating app/__init__.py to use blueprint..."
cat > app/__init__.py << 'INIT_EOF2'
from flask import Flask
from flask_restx import Api

def create_app():
    app = Flask(__name__)
    
    # Import and register the API blueprint
    try:
        from .api.v1.routes import blueprint as api_v1_blueprint
        app.register_blueprint(api_v1_blueprint)
    except ImportError:
        # Fallback if routes aren't ready
        api = Api(app, version='1.0', title='HBnB API', 
                 description='HBnB Application API', doc='/api/v1/')
    
    return app
INIT_EOF2

# Step 6: Create persistence/repository.py
echo "8. Creating persistence/repository.py..."
cat > app/persistence/repository.py << 'REPO_EOF'
from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)
REPO_EOF

# Step 7: Create services/facade.py
echo "9. Creating services/facade.py..."
cat > app/services/facade.py << 'FACADE_EOF'
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder method for creating a user
    def create_user(self, user_data):
        # Logic will be implemented in later tasks
        pass

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass
FACADE_EOF

# Step 8: Create run.py
echo "10. Creating run.py..."
cat > run.py << 'RUN_EOF'
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
RUN_EOF

echo "=== Restructuring Complete ==="
echo "Project structure has been updated to match Task 00 requirements."
