"""API v1 routes configuration."""
from flask_restx import Namespace, Resource

# Main API namespace
api = Namespace('api', description='HBnB API operations')

# Import namespaces
from .user_routes import api as user_ns
from .amenity_routes import api as amenity_ns
from .place_routes import api as place_ns
from .review_routes import api as review_ns
from .errors import api as error_ns

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
