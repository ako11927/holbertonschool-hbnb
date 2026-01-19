"""Amenity model for place amenities."""
from typing import List, Dict, Any
from .base_model import BaseModel
from ..exceptions import ValidationError


class Amenity(BaseModel):
    """
    Amenity model representing features available at a place.
    
    Attributes:
        name (str): Name of the amenity (e.g., "WiFi", "Pool")
        description (str): Optional description of the amenity
        icon (str): Optional icon name for UI display
        category (str): Category of amenity (e.g., "basic", "safety", "luxury")
    """
    
    # Predefined categories for consistency
    CATEGORIES = ['basic', 'safety', 'luxury', 'accessibility', 'kitchen', 'bathroom']
    
    def __init__(self, **kwargs):
        """
        Initialize amenity with validation.
        
        Args:
            **kwargs: Amenity attributes including:
                name: Required
                description: Optional
                icon: Optional
                category: Optional, must be one of predefined categories
        """
        super().__init__(**kwargs)
        self.name = kwargs.get('name', '')
        self.description = kwargs.get('description', '')
        self.icon = kwargs.get('icon', '')
        self.category = kwargs.get('category', 'basic')
        
        # Validate required fields
        if not self.name:
            raise ValidationError("Name is required")
        
        # Validate category
        if self.category not in self.CATEGORIES:
            raise ValidationError(
                f"Category must be one of: {', '.join(self.CATEGORIES)}"
            )
    
    @property
    def category(self) -> str:
        """Get category."""
        return self._category
    
    @category.setter
    def category(self, value: str):
        """Set category with validation."""
        if value not in self.CATEGORIES:
            raise ValidationError(
                f"Category must be one of: {', '.join(self.CATEGORIES)}"
            )
        self._category = value
        self.save()
    
    @classmethod
    def get_categories(cls) -> List[str]:
        """
        Get list of valid amenity categories.
        
        Returns:
            List of category names
        """
        return cls.CATEGORIES.copy()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert amenity to dictionary.
        
        Returns:
            Dictionary representation
        """
        result = super().to_dict()
        return result
