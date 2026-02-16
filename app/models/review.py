from app import db
from .base_model import BaseModel

class Review(BaseModel):
    """SQLAlchemy model representing a user's review of a place."""

    __tablename__ = 'reviews'

    # Foreign keys
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    # Core attributes
    text = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Integer, nullable=False)

    # ========== Relationships ==========
    # Many-to-One: Review → User
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))

    # Many-to-One: Review → Place
    place = db.relationship('Place', backref=db.backref('reviews', lazy=True))

    # ========== Methods ==========
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.user_id:
            raise ValueError("user_id is required")
        if not self.place_id:
            raise ValueError("place_id is required")
        if not (1 <= self.rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

    @property
    def summary(self) -> str:
        """Return a short summary of the review."""
        if not self.text:
            return f"Rating: {self.rating}/5"
        summary_text = self.text[:100]
        if len(self.text) > 100:
            summary_text += "..."
        return f"Rating: {self.rating}/5 - {summary_text}"
