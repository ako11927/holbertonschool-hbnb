"""Review repository for database operations with relationships."""
from app.models.review import Review
from app.repositories.base_repository import BaseRepository


class ReviewRepository(BaseRepository):
    """Repository for Review model operations with relationships."""
    
    def __init__(self):
        """Initialize ReviewRepository with Review model."""
        super().__init__(Review)
    
    def create_review(self, review_data):
        """Create a new review with user and place relationships."""
        # Check if user has already reviewed this place
        existing_review = self.get_by_user_and_place(
            review_data['user_id'], 
            review_data['place_id']
        )
        if existing_review:
            raise ValueError("User has already reviewed this place")
        
        # Create review instance
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user_id=review_data['user_id'],
            place_id=review_data['place_id']
        )
        
        # Save to database
        return self.add(review)
    
    def get_review_with_relationships(self, review_id):
        """Get a review with all relationships loaded."""
        from sqlalchemy.orm import joinedload
        review = self.model.query.options(
            joinedload(Review.user),
            joinedload(Review.place)
        ).get(review_id)
        return review
    
    def get_by_user_and_place(self, user_id, place_id):
        """Get review by user and place."""
        return self.model.query.filter_by(
            user_id=user_id, 
            place_id=place_id
        ).first()
    
    def get_reviews_by_user(self, user_id):
        """Get all reviews by a user."""
        return self.model.query.filter_by(user_id=user_id).all()
    
    def get_reviews_by_place(self, place_id):
        """Get all reviews for a place."""
        return self.model.query.filter_by(place_id=place_id).all()
    
    def get_reviews_by_rating(self, rating):
        """Get all reviews with a specific rating."""
        return self.model.query.filter_by(rating=rating).all()
    
    def get_reviews_in_rating_range(self, min_rating, max_rating):
        """Get reviews within a rating range."""
        return self.model.query.filter(
            Review.rating >= min_rating,
            Review.rating <= max_rating
        ).all()
    
    def get_recent_reviews(self, limit=10):
        """Get most recent reviews."""
        return self.model.query.order_by(Review.created_at.desc()).limit(limit).all()
    
    def get_average_rating_for_place(self, place_id):
        """Get average rating for a place."""
        from sqlalchemy import func
        result = db.session.query(func.avg(Review.rating)).filter_by(place_id=place_id).scalar()
        return float(result) if result else 0.0
