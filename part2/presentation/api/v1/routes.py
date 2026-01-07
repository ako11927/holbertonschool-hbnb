"""API v1 routes configuration."""
from flask_restx import Api, Resource
from .errors import default_error_handler, not_found_error_handler, bad_request_error_handler

# Create main API instance
api = Api(
    version='1.0',
    title='HBnB API',
    description='HBnB API operations',
    doc='/api/v1/docs'
)

# Register error handlers
api.errorhandler(Exception)(default_error_handler)
api.errorhandler(404)(not_found_error_handler)
api.errorhandler(400)(bad_request_error_handler)

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
        """Get API status."""
        return {'status': 'OK', 'version': '1.0'}
