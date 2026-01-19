"""City model."""
from typing import Dict, Any
from .base_model import BaseModel
from ..exceptions import ValidationError


class City(BaseModel):
    """
    City model representing a geographical city.
    
    Attributes:
        name (str): Name of the city
        state_id (str): ID of the state containing the city
    """
    
    def __init__(self, **kwargs):
        """
        Initialize city with validation.
        
        Args:
            **kwargs: City attributes including:
                name: Required
                state_id: Required
        """
        super().__init__(**kwargs)
        self.name = kwargs.get('name', '')
        self.state_id = kwargs.get('state_id', '')
        
        # Validate required fields
        if not self.name:
            raise ValidationError("Name is required")
        if not self.state_id:
            raise ValidationError("state_id is required")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert city to dictionary.
        
        Returns:
            Dictionary representation
        """
        result = super().to_dict()
        return result
