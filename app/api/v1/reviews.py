from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    def post(self):
        """Create a review (cannot review own place, only one review per place)"""
        user_id = get_jwt_identity()
        data = api.payload
        place = facade.get_place(data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 404
        if place.owner_id == user_id:
            return {'error': 'You cannot review your own place'}, 400
        existing = facade.get_user_review_for_place(user_id, data['place_id'])
        if existing:
            return {'error': 'You have already reviewed this place'}, 400
        data['user_id'] = user_id
        review = facade.create_review(data)
        return {'id': review.id, 'text': review.text}, 201

@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @jwt_required()
    def put(self, review_id):
        """Update review (creator or admin)"""
        user_claims = get_jwt()
        user_id = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if not user_claims.get('is_admin', False) and review.user_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        updated = facade.update_review(review_id, api.payload)
        return {'id': updated.id, 'text': updated.text}, 200

    @jwt_required()
    def delete(self, review_id):
        """Delete review (creator or admin)"""
        user_claims = get_jwt()
        user_id = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if not user_claims.get('is_admin', False) and review.user_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_review(review_id)
        return {'message': 'Review deleted'}, 200
