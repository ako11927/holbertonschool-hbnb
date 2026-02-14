"""Review service for business logic."""
from app.services.facade import HBnBFacade


class ReviewService:
    """Service for review operations."""
    
    def __init__(self):
        """Initialize service with facade."""
        self.facade = HBnBFacade()
    
    def create_review(self, review_data):
        """Create a new review."""
        try:
            # Validate required fields
            required_fields = ['text', 'rating']
            for field in required_fields:
                if not review_data.get(field):
                    return {'error': f'{field} is required'}, 400
            
            # Create review via facade
            review = self.facade.create_review(review_data)
            return review.to_dict(), 201
        
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Failed to create review'}, 500
    
    def get_review(self, review_id):
        """Get a review by ID."""
        review = self.facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200
    
    def get_all_reviews(self):
        """Get all reviews."""
        reviews = self.facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200
    
    def update_review(self, review_id, review_data):
        """Update a review."""
        try:
            review = self.facade.update_review(review_id, review_data)
            if not review:
                return {'error': 'Review not found'}, 404
            return review.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
    
    def delete_review(self, review_id):
        """Delete a review."""
        success = self.facade.delete_review(review_id)
        if not success:
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted successfully'}, 200
    
    def get_reviews_by_rating(self, rating):
        """Get reviews by rating."""
        try:
            rating_int = int(rating)
            if rating_int < 1 or rating_int > 5:
                return {'error': 'Rating must be between 1 and 5'}, 400
            
            reviews = self.facade.get_reviews_by_rating(rating_int)
            return [review.to_dict() for review in reviews], 200
        except (ValueError, TypeError):
            return {'error': 'Rating must be a valid integer'}, 400
    
    def get_recent_reviews(self, limit=10):
        """Get recent reviews."""
        reviews = self.facade.get_recent_reviews(limit)
        return [review.to_dict() for review in reviews], 200
