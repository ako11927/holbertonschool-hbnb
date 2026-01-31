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
    doc='/docs'  # This will be at /api/v1/docs
)

# Import namespaces
from .user_routes import api as user_ns
from .amenity_routes import api as amenity_ns
from .place_routes import api as place_ns
from .review_routes import api as review_ns

# Add all namespaces to the main API
api.add_namespace(user_ns, path='/users')
api.add_namespace(amenity_ns, path='/amenities')
api.add_namespace(place_ns, path='/places')
api.add_namespace(review_ns, path='/reviews')

# Status endpoint
@api.route('/status')
class Status(Resource):
    """API status endpoint."""
    def get(self):
        return {'status': 'OK', 'version': '1.0'}
