"""Review model for user reviews of places."""
from typing import Dict, Any
from datetime import datetime
from .base_model import BaseModel
from ..exceptions import ValidationError


class Review(BaseModel):
    """
    Review model representing a user's review of a place.
    
    Attributes:
        user_id (str): ID of the user who wrote the review
        place_id (str): ID of the place being reviewed
        text (str): Review text content
        rating (int): Rating from 1 to 5
    """
    
    def __init__(self, **kwargs):
        """
        Initialize review with validation.
        
        Args:
            **kwargs: Review attributes including:
                user_id: Required
                place_id: Required
                text: Optional review text
                rating: Required, between 1 and 5
        """
        super().__init__(**kwargs)
        self.user_id = kwargs.get('user_id', '')
        self.place_id = kwargs.get('place_id', '')
        self.text = kwargs.get('text', '')
        self.rating = kwargs.get('rating', 0)
        
        # Validate required fields
        if not self.user_id:
            raise ValidationError("user_id is required")
        if not self.place_id:
            raise ValidationError("place_id is required")
        
        # Validate rating
        if self.rating < 1 or self.rating > 5:
            raise ValidationError("Rating must be between 1 and 5")
    
    @property
    def rating(self) -> int:
        """Get rating."""
        return self._rating
    
    @rating.setter
    def rating(self, value: int):
        """Set rating with validation."""
        value = int(value)
        if value < 1 or value > 5:
            raise ValidationError("Rating must be between 1 and 5")
        self._rating = value
        self.save()
    
    @property
    def summary(self) -> str:
        """
        Get a summary of the review.
        
        Returns:
            Summary string
        """
        if not self.text:
            return f"Rating: {self.rating}/5"
        
        # Get first 100 characters for summary
        summary_text = self.text[:100]
        if len(self.text) > 100:
            summary_text += "..."
        return f"Rating: {self.rating}/5 - {summary_text}"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert review to dictionary.
        
        Returns:
            Dictionary representation
        """
        result = super().to_dict()
        result['rating'] = self.rating
        result['summary'] = self.summary
        return result
