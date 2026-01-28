from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services import facade
from app.utils.auth_helpers import is_current_user_admin

api = Namespace('places', description='Place operations')

# Define models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})
  
user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Define the place model for input validation and documentation
place_input_model = api.model('PlaceInput', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(description='Set automatically from JWT'),
    'amenities': fields.List(fields.String, description="List of amenities ID's")
})

place_create_input_model = api.model('PlaceCreateInput', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, description="List of amenities ID's")
})

place_model = api.model('Place', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'owner_id': fields.String(description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp')
})

place_summary_model = api.model('PlaceSummary', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_create_input_model)
    @api.response(201, 'Place successfully created', place_model)
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @jwt_required()
    def post(self):
        """Register a new place (authenticated users only). Admin can set any owner_id; non-admin is owner."""
        try:
            data = request.get_json() or {}
            current_id = str(get_jwt_identity())
            if not is_current_user_admin():
                data['owner_id'] = current_id
            elif 'owner_id' not in data:
                data['owner_id'] = current_id

            required_fields = ['title', 'price', 'latitude', 'longitude']
            for field in required_fields:
                if field not in data:
                    return {'error': f'Missing required field: {field}'}, 400

            place = facade.create_place(data)
            return place.to_dict(), 201

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500

    @api.response(200, 'List of places retrieved successfully')
    @api.marshal_list_with(place_summary_model)
    def get(self):
        """Retrieve a list of all places (public)."""
        places = facade.get_all_places()
        return [
            {
                'id': place.id,
                'title': getattr(place, 'title', ''),
                'latitude': getattr(place, 'latitude', 0.0),
                'longitude': getattr(place, 'longitude', 0.0),
            }
            for place in places
        ]

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully', place_model)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID (public)."""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict(), 200

    @api.expect(place_input_model)
    @api.response(200, 'Place updated successfully')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information (owner or admin)."""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        current_id = str(get_jwt_identity())
        owner_id = str(getattr(place, 'owner_id', ''))
        if not is_current_user_admin() and current_id != owner_id:
            return {'error': 'You can only modify your own places'}, 403
        try:
            data = request.get_json() or {}
            updated_place = facade.update_place(place_id, data)
            if not updated_place:
                return {'error': 'Place not found'}, 404
            return {'message': 'Place updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500

    @api.response(204, 'Place deleted successfully')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Place not found')
    @api.response(401, 'Authentication required')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place (owner or admin)."""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        current_id = str(get_jwt_identity())
        owner_id = str(getattr(place, 'owner_id', ''))
        if not is_current_user_admin() and current_id != owner_id:
            return {'error': 'You can only delete your own places'}, 403
        facade.place_repo.delete(place_id)
        return '', 204

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        # Check if place exists
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        reviews = facade.get_reviews_by_place(place_id)
        
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id
            }
            for review in reviews
        ], 200
