"""Review routes namespace."""
from flask_restx import Namespace, Resource

# Create namespace
api = Namespace('reviews', description='Review operations')

@api.route('/')
class ReviewList(Resource):
    """List all reviews or create new review."""
    def get(self):
        """Get all reviews."""
        return {'message': 'GET /reviews'}, 200
    
    def post(self):
        """Create a new review."""
        return {'message': 'POST /reviews'}, 201

@api.route('/<review_id>')
class ReviewDetail(Resource):
    """Get, update, or delete specific review."""
    def get(self, review_id):
        """Get review by ID."""
        return {'message': f'GET /reviews/{review_id}'}, 200
    
    def put(self, review_id):
        """Update review by ID."""
        return {'message': f'PUT /reviews/{review_id}'}, 200
    
    def delete(self, review_id):
        """Delete review by ID."""
        return {'message': f'DELETE /reviews/{review_id}'}, 204
