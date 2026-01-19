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
    
    # Import and register namespaces directly (as shown in Task 02)
    try:
        from .api.v1.users import api as users_ns
        from .api.v1.places import api as places_ns
        from .api.v1.reviews import api as reviews_ns
        from .api.v1.amenities import api as amenities_ns
        
        api.add_namespace(users_ns, path='/api/v1/users')
        api.add_namespace(places_ns, path='/api/v1/places')
        api.add_namespace(reviews_ns, path='/api/v1/reviews')
        api.add_namespace(amenities_ns, path='/api/v1/amenities')
        
        print("✅ All API namespaces registered")
    except ImportError as e:
        print(f"⚠️ Could not import all namespaces: {e}")
    
    return app
