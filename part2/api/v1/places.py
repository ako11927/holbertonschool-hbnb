from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade

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
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
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
    @api.expect(place_input_model)
    @api.response(201, 'Place successfully created', place_model)
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['title', 'price', 'latitude', 'longitude', 'owner_id']
            for field in required_fields:
                if field not in data:
                    return {'error': f'Missing required field: {field}'}, 400
            
            # Create place
            place = facade.create_place(data)
            
            return place.to_dict(), 201
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500

    @api.response(200, 'List of places retrieved successfully')
    @api.marshal_list_with(place_summary_model)
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        
        # Return summary for list view
        return [
            {
                'id': place.id,
                'title': place.title,
                'latitude': place.latitude,
                'longitude': place.longitude
            }
            for place in places
        ]

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully', place_model)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        return place.to_dict(), 200

    @api.expect(place_input_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        try:
            data = request.get_json()
            
            # Check if place exists
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404
            
            # Update place
            updated_place = facade.update_place(place_id, data)
            if not updated_place:
                return {'error': 'Place not found'}, 404
            
            return {'message': 'Place updated successfully'}, 200
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500

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
