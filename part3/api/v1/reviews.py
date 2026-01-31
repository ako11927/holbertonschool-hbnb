from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_input_model = api.model('ReviewInput', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
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
    @jwt_required()
    @api.expect(review_input_model)
    @api.response(201, 'Review successfully created', review_model)
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Non-admin can only set user_id to self')
    def post(self):
        """Register a new review. JWT required. Non-admin can only set user_id to self; admin can set any."""
        try:
            data = request.get_json() or {}
            uid = get_jwt_identity()
            is_admin = get_jwt().get('is_admin') is True
            if not is_admin and data.get('user_id') != uid:
                return {'error': 'Non-admin can only create reviews with user_id equal to your user id'}, 403
            review = facade.create_review(data)
            return review.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500

    @api.response(200, 'List of reviews retrieved successfully')
    @api.marshal_list_with(review_summary_model)
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        
        # Return summary for list view
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating
            }
            for review in reviews
        ]

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully', review_model)
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        return review.to_dict(), 200

    @jwt_required()
    @api.expect(review_input_model)
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Only author or admin can update')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review. JWT required. Only author or admin; admins bypass ownership."""
        try:
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Review not found'}, 404
            uid = get_jwt_identity()
            is_admin = get_jwt().get('is_admin') is True
            if not is_admin and getattr(review, 'user_id', None) != uid:
                return {'error': 'Only the review author or an admin can update this review'}, 403
            data = request.get_json() or {}
            updated_review = facade.update_review(review_id, data)
            if not updated_review:
                return {'error': 'Review not found'}, 404
            return {'message': 'Review updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Only author or admin can delete')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review. JWT required. Only author or admin; admins bypass ownership."""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        uid = get_jwt_identity()
        is_admin = get_jwt().get('is_admin') is True
        if not is_admin and getattr(review, 'user_id', None) != uid:
            return {'error': 'Only the review author or an admin can delete this review'}, 403
        success = facade.delete_review(review_id)
        if not success:
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 200
