from flask import Blueprint
from flask_restx import Api

# Create Blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Create API
api = Api(api_bp,
          title='HBnB API',
          version='1.0',
          description='A REST API for HBnB clone',
          doc='/docs')

# Import and register namespaces
try:
    from .v1.users import api as users_ns
    api.add_namespace(users_ns, path='/users')
except ImportError:
    pass

try:
    from .v1.places import api as places_ns
    api.add_namespace(places_ns, path='/places')
except ImportError:
    pass

try:
    from .v1.reviews import api as reviews_ns
    api.add_namespace(reviews_ns, path='/reviews')
except ImportError:
    pass
