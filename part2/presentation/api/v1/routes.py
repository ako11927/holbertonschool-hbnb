"""API v1 routes configuration."""
from flask_restx import Namespace
from .user_routes import api as user_ns
from .amenity_routes import api as amenity_ns
from .place_routes import api as place_ns
from .review_routes import api as review_ns
from .errors import api as error_ns

# Main API namespace
api = Namespace('api', description='HBnB API operations')

# Import models from each namespace to make them available globally
# This allows cross-referencing models between namespaces
from .user_routes import user_model
from .amenity_routes import amenity_model
from .place_routes import place_model, place_with_relationships_model
from .review_routes import review_model, review_with_user_model

# Add all namespaces
api.add_namespace(user_ns, path='/users')
api.add_namespace(amenity_ns, path='/amenities')
api.add_namespace(place_ns, path='/places')
api.add_namespace(review_ns, path='/reviews')

# Status endpoint
@api.route('/status')
class Status(Resource):
    """API status endpoint."""
    def get(self):
        """Get API status."""
        return {'status': 'OK', 'version': '1.0'}

# Import Resource after creating api to avoid circular import
from flask_restx import Resource
