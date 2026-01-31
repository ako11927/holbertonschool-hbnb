"""Review model with relationships."""
from app import db
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates


class Review(BaseModel):
    """Review model representing a user review."""
    __tablename__ = 'reviews'
    
    # Core attributes
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    
    # Foreign Keys
    # One-to-Many: User -> Reviews (a review is written by one user)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # One-to-Many: Place -> Reviews (a review is for one place)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    
    # Relationships
    # Many-to-One: Review -> User (a review belongs to one user)
    user = db.relationship('User', back_populates='reviews')
    
    # Many-to-One: Review -> Place (a review belongs to one place)
    place = db.relationship('Place', back_populates='reviews')
    
    @validates('text')
    def validate_text(self, key, text):
        """Validate review text."""
        if not text or not text.strip():
            raise ValueError("Review text is required")
        if len(text.strip()) < 10:
            raise ValueError("Review text must be at least 10 characters")
        return text.strip()
    
    @validates('rating')
    def validate_rating(self, key, rating):
        """Validate rating (1-5)."""
        if rating is None:
            raise ValueError("Rating is required")
        
        try:
            rating_int = int(rating)
            if rating_int < 1 or rating_int > 5:
                raise ValueError("Rating must be between 1 and 5")
            return rating_int
        except (ValueError, TypeError):
            raise ValueError("Rating must be a valid integer between 1 and 5")
    
    def to_dict(self):
        """Convert review object to dictionary."""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_with_relationships(self):
        """Convert review object to dictionary with relationships."""
        result = self.to_dict()
        
        # Include user information
        if self.user:
            result['user'] = self.user.to_dict_without_email()
        
        # Include place information
        if self.place:
            result['place'] = {
                'id': self.place.id,
                'title': self.place.title,
                'city': self.place.city
            }
        
        return result
    
    def __repr__(self):
        return f'<Review {self.rating} stars>'
