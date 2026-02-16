from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.services import facade

api = Namespace('places', description='Place operations')

@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    def post(self):
        """Create a new place (owner = logged-in user)"""
        user_id = get_jwt_identity()
        data = api.payload
        data['owner_id'] = user_id
        new_place = facade.create_place(data)
        return {'id': new_place.id, 'title': new_place.title}, 201

@api.route('/<string:place_id>')
class PlaceResource(Resource):
    @jwt_required()
    def put(self, place_id):
        """Update place (owner or admin)"""
        user_claims = get_jwt()
        user_id = get_jwt_identity()
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if not user_claims.get('is_admin', False) and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        updated_place = facade.update_place(place_id, api.payload)
        return {'id': updated_place.id, 'title': updated_place.title}, 200

    @jwt_required()
    def delete(self, place_id):
        """Delete place (owner or admin)"""
        user_claims = get_jwt()
        user_id = get_jwt_identity()
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if not user_claims.get('is_admin', False) and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_place(place_id)
        return {'message': 'Place deleted'}, 200
