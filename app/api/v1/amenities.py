from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {'name': fields.String(required=True)})

@api.route('/')
class AmenityList(Resource):
    @jwt_required()
    def post(self):
        """Create a new amenity (Admins only)"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403
        data = api.payload
        amenity = facade.create_amenity(data)
        return {'id': amenity.id, 'name': amenity.name}, 201

    def get(self):
        """List all amenities (public)"""
        amenities = facade.get_all_amenities()
        return [{'id': a.id, 'name': a.name} for a in amenities], 200

@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity (Admins only)"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403
        data = api.payload
        amenity = facade.update_amenity(amenity_id, data)
        return {'id': amenity.id, 'name': amenity.name}, 200
