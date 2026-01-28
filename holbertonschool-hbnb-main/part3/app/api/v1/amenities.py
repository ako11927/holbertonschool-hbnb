"""Amenity API endpoints."""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required

from app.services import facade
from app.utils.auth_helpers import is_current_user_admin

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Admin required')
    @jwt_required()
    def post(self):
        """Register a new amenity (admin only)."""
        if not is_current_user_admin():
            return {'error': 'Admin access required'}, 403
        amenity_data = api.payload
        new_amenity = facade.create_amenity(amenity_data)
        return {
            'id': new_amenity.id,
            'name': new_amenity.name
        }, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities (public)."""
        amenities = facade.get_all_amenities()
        return [
            {'id': amenity.id, 'name': amenity.name}
            for amenity in amenities
        ], 200


@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID (public)."""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Admin required')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information (admin only)."""
        if not is_current_user_admin():
            return {'error': 'Admin access required'}, 403
        amenity_data = api.payload
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        if not updated_amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': updated_amenity.id, 'name': updated_amenity.name}, 200
