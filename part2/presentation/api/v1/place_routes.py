"""Place routes namespace."""
from flask_restx import Namespace, Resource

# Create namespace
api = Namespace('places', description='Place operations')

@api.route('/')
class PlaceList(Resource):
    """List all places or create new place."""
    def get(self):
        """Get all places."""
        return {'message': 'GET /places'}, 200
    
    def post(self):
        """Create a new place."""
        return {'message': 'POST /places'}, 201

@api.route('/<place_id>')
class PlaceDetail(Resource):
    """Get, update, or delete specific place."""
    def get(self, place_id):
        """Get place by ID."""
        return {'message': f'GET /places/{place_id}'}, 200
    
    def put(self, place_id):
        """Update place by ID."""
        return {'message': f'PUT /places/{place_id}'}, 200
    
    def delete(self, place_id):
        """Delete place by ID."""
        return {'message': f'DELETE /places/{place_id}'}, 204
