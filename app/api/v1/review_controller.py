"""Review controller for handling review-related API requests."""
from flask import request, jsonify
from app.services.review_service import ReviewService


class ReviewController:
    """Controller for review endpoints."""
    
    def __init__(self):
        """Initialize controller with service."""
        self.review_service = ReviewService()
    
    def get_reviews(self):
        """Get all reviews."""
        reviews, status_code = self.review_service.get_all_reviews()
        return jsonify(reviews), status_code
    
    def get_review(self, review_id):
        """Get a specific review."""
        result, status_code = self.review_service.get_review(review_id)
        return jsonify(result), status_code
    
    def create_review(self):
        """Create a new review."""
        review_data = request.get_json()
        
        if not review_data:
            return jsonify({'error': 'No input data provided'}), 400
        
        result, status_code = self.review_service.create_review(review_data)
        return jsonify(result), status_code
    
    def update_review(self, review_id):
        """Update a review."""
        review_data = request.get_json()
        
        if not review_data:
            return jsonify({'error': 'No input data provided'}), 400
        
        result, status_code = self.review_service.update_review(review_id, review_data)
        return jsonify(result), status_code
    
    def delete_review(self, review_id):
        """Delete a review."""
        result, status_code = self.review_service.delete_review(review_id)
        return jsonify(result), status_code
    
    def get_reviews_by_rating(self):
        """Get reviews by rating."""
        rating = request.args.get('rating')
        if not rating:
            return jsonify({'error': 'Rating is required'}), 400
        
        reviews, status_code = self.review_service.get_reviews_by_rating(rating)
        return jsonify(reviews), status_code
    
    def get_recent_reviews(self):
        """Get recent reviews."""
        limit = request.args.get('limit', 10)
        try:
            limit_int = int(limit)
            if limit_int < 1 or limit_int > 100:
                return jsonify({'error': 'Limit must be between 1 and 100'}), 400
        except ValueError:
            return jsonify({'error': 'Limit must be a valid integer'}), 400
        
        reviews, status_code = self.review_service.get_recent_reviews(limit_int)
        return jsonify(reviews), status_code
