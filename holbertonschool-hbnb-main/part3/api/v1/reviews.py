from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services import facade
from app.utils.auth_helpers import is_current_user_admin

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_input_model = api.model('ReviewInput', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(description='Set automatically from JWT'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_create_input_model = api.model('ReviewCreateInput', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_model = api.model('Review', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user'),
    'place_id': fields.String(description='ID of the place'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp')
})

review_summary_model = api.model('ReviewSummary', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_create_input_model)
    @api.response(201, 'Review successfully created', review_model)
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @jwt_required()
    def post(self):
        """Register a new review (authenticated users only). Admin bypasses own-place and duplicate rules."""
        try:
            data = request.get_json() or {}
            current_id = str(get_jwt_identity())
            if not is_current_user_admin():
                data['user_id'] = current_id

            place_id = data.get('place_id')
            if not place_id:
                return {'error': 'place_id is required'}, 400
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404

            user_id = str(data.get('user_id', current_id))
            if not is_current_user_admin():
                owner_id = str(getattr(place, 'owner_id', ''))
                if current_id == owner_id:
                    return {'error': 'You cannot review your own place'}, 400
                existing = facade.get_reviews_by_place(place_id)
                if any(str(getattr(r, 'user_id', '')) == current_id for r in existing):
                    return {'error': 'You have already reviewed this place'}, 400
            else:
                data['user_id'] = user_id if user_id else current_id

            review = facade.create_review(data)
            return review.to_dict(), 201

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500

    @api.response(200, 'List of reviews retrieved successfully')
    @api.marshal_list_with(review_summary_model)
    def get(self):
        """Retrieve a list of all reviews (public)."""
        reviews = facade.get_all_reviews()
        return [
            {
                'id': review.id,
                'text': getattr(review, 'text', ''),
                'rating': getattr(review, 'rating', 0),
            }
            for review in reviews
        ]

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully', review_model)
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID (public)."""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @api.expect(review_input_model)
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information (author or admin)."""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        current_id = str(get_jwt_identity())
        author_id = str(getattr(review, 'user_id', ''))
        if not is_current_user_admin() and current_id != author_id:
            return {'error': 'You can only modify your own reviews'}, 403
        try:
            data = request.get_json() or {}
            updated_review = facade.update_review(review_id, data)
            if not updated_review:
                return {'error': 'Review not found'}, 404
            return {'message': 'Review updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500

    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Review not found')
    @api.response(401, 'Authentication required')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review (author or admin)."""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        current_id = str(get_jwt_identity())
        author_id = str(getattr(review, 'user_id', ''))
        if not is_current_user_admin() and current_id != author_id:
            return {'error': 'You can only delete your own reviews'}, 403
        success = facade.delete_review(review_id)
        if not success:
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 200
