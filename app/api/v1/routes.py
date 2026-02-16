"""API v1 routes configuration with namespaces and JWT."""

from flask import Blueprint
from flask_restx import Api

# Import namespaces
from .users import api as users_ns
from .places import api as places_ns
from .reviews import api as reviews_ns
from .amenities import api as amenities_ns
from .auth import api as auth_ns

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

# Register namespaces
api.add_namespace(users_ns, path='/users')
api.add_namespace(places_ns, path='/places')
api.add_namespace(reviews_ns, path='/reviews')
api.add_namespace(amenities_ns, path='/amenities')
api.add_namespace(auth_ns, path='/auth')

# Status endpoint
@api.route('/status')
class Status(Resource):
    """API status endpoint."""
    def get(self):
        return {'status': 'OK', 'version': '1.0'}
