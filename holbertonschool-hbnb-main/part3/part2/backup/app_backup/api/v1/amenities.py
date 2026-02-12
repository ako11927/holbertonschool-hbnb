"""Amenity routes namespace."""
from flask_restx import Namespace, Resource

# Create namespace
api = Namespace('amenities', description='Amenity operations')

@api.route('/')
class AmenityList(Resource):
    """List all amenities or create new amenity."""
    def get(self):
        """Get all amenities."""
        return {'message': 'GET /amenities'}, 200
    
    def post(self):
        """Create a new amenity."""
        return {'message': 'POST /amenities'}, 201

@api.route('/<amenity_id>')
class AmenityDetail(Resource):
    """Get, update, or delete specific amenity."""
    def get(self, amenity_id):
        """Get amenity by ID."""
        return {'message': f'GET /amenities/{amenity_id}'}, 200
    
    def put(self, amenity_id):
        """Update amenity by ID."""
        return {'message': f'PUT /amenities/{amenity_id}'}, 200
    
    def delete(self, amenity_id):
        """Delete amenity by ID."""
        return {'message': f'DELETE /amenities/{amenity_id}'}, 204
