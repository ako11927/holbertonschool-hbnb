"""Review API endpoints."""
from flask_restx import Namespace, Resource, fields, reqparse
from business_logic.facade import HBnBFacade
from business_logic.exceptions import ValidationError, NotFoundError, DuplicateError

api = Namespace('reviews', description='Review operations')

# Request parsers
review_parser = reqparse.RequestParser()
review_parser.add_argument('user_id', type=str, required=True, help='User ID')
review_parser.add_argument('place_id', type=str, required=True, help='Place ID')
review_parser.add_argument('text', type=str, required=True, help='Review text')
review_parser.add_argument('rating', type=int, required=True, help='Rating (1-5)')

update_review_parser = reqparse.RequestParser()
update_review_parser.add_argument('text', type=str, required=False, help='Review text')
update_review_parser.add_argument('rating', type=int, required=False, help='Rating (1-5)')

# Response models
review_model = api.model('Review', {
    'id': fields.String(description='Review ID'),
    'user_id': fields.String(description='User ID'),
    'place_id': fields.String(description='Place ID'),
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating (1-5)'),
    'summary': fields.String(description='Review summary'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Update timestamp')
})

    'id': fields.String(description='Review ID'),
    'place_id': fields.String(description='Place ID'),
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating (1-5)'),
    'summary': fields.String(description='Review summary'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Update timestamp')
})

facade = HBnBFacade()

@api.route('/')
class ReviewList(Resource):
    @api.doc('list_reviews')
    @api.marshal_list_with(review_model)
    def get(self):
        """
        Retrieve all reviews.
        
        Returns:
            List of all reviews
        """
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200

    @api.doc('create_review')
    @api.expect(review_parser)
    @api.marshal_with(review_model, code=201)
    @api.response(400, 'Invalid input')
    @api.response(404, 'User or Place not found')
    @api.response(409, 'User already reviewed this place')
    def post(self):
        """
        Create a new review.
        
        Returns:
            Created review data
        """
        args = review_parser.parse_args()
        
        # Validate rating
        if args['rating'] < 1 or args['rating'] > 5:
            api.abort(400, 'Rating must be between 1 and 5')
        
        try:
            review = facade.create_review(args)
            return review.to_dict(), 201
        except ValidationError as e:
            api.abort(400, str(e))
        except NotFoundError as e:
            api.abort(404, str(e))
        except DuplicateError as e:
            api.abort(409, str(e))
        except Exception as e:
            api.abort(500, 'Internal server error')

@api.route('/<string:review_id>')
@api.param('review_id', 'The review identifier')
@api.response(404, 'Review not found')
class ReviewResource(Resource):
    @api.doc('get_review')
    def get(self, review_id):
        """
        Retrieve a review by ID with user details.
        
        Args:
            review_id: Review identifier
            
        Returns:
            Review data with user information
        """
        review = facade.review_repository.get(review_id)
        if not review:
            api.abort(404, f'Review {review_id} not found')
        
        # Get user details
        user = facade.get_user(review.user_id)
        
        # Build response
        response = review.to_dict()
        response['user'] = user.to_dict() if user else None
        
        return response, 200

    @api.doc('update_review')
    @api.expect(update_review_parser)
    @api.marshal_with(review_model)
    @api.response(400, 'Invalid input')
    def put(self, review_id):
        """
        Update review information.
        
        Args:
            review_id: Review identifier
            
        Returns:
            Updated review data
        """
        args = update_review_parser.parse_args()
        
        # Remove None values
        update_data = {k: v for k, v in args.items() if v is not None}
        
        if not update_data:
            api.abort(400, 'No update data provided')
        
        # Get existing review
        review = facade.review_repository.get(review_id)
        if not review:
            api.abort(404, f'Review {review_id} not found')
        
        try:
            # Validate rating if provided
            if 'rating' in update_data and (update_data['rating'] < 1 or update_data['rating'] > 5):
                api.abort(400, 'Rating must be between 1 and 5')
            
            # Update review attributes
            for key, value in update_data.items():
                if hasattr(review, key):
                    setattr(review, key, value)
            
            # Save the review
            review.save()
            
            # Update in repository
            facade.review_repository.update(review_id, review.to_dict())
            
            return review.to_dict(), 200
        except ValidationError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, 'Internal server error')

    @api.doc('delete_review')
    @api.response(204, 'Review deleted')
    def delete(self, review_id):
        """
        Delete a review.
        
        Args:
            review_id: Review identifier
            
        Returns:
            No content
        """
        review = facade.review_repository.get(review_id)
        if not review:
            api.abort(404, f'Review {review_id} not found')
        
        try:
            # Delete from repository
            facade.review_repository.delete(review_id)
            
            # Remove from relationship caches
            for user_id, review_ids in facade._user_reviews.items():
                if review_id in review_ids:
                    review_ids.remove(review_id)
                    break
            
            for place_id, review_ids in facade._place_reviews.items():
                if review_id in review_ids:
                    review_ids.remove(review_id)
                    break
            
            return '', 204
        except Exception as e:
            api.abort(500, 'Internal server error')
