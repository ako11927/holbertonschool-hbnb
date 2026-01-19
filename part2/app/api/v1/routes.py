"""API v1 routes configuration."""
from flask_restx import Resource

# Status endpoint (minimal - namespaces are registered in app/__init__.py)
from flask import Blueprint
from flask_restx import Api

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

# Status endpoint
@api.route('/status')
class Status(Resource):
    """API status endpoint."""
    def get(self):
        return {'status': 'OK', 'version': '1.0'}
