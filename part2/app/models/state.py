"""State model."""
from typing import Dict, Any, List
from .base_model import BaseModel
from ..exceptions import ValidationError


class State(BaseModel):
    """
    State model representing a geographical state/province.
    
    Attributes:
        name (str): Name of the state
        cities (list): List of cities in this state
    """
    
    def __init__(self, **kwargs):
        """
        Initialize state with validation.
        
        Args:
            **kwargs: State attributes including:
                name: Required
        """
        super().__init__(**kwargs)
        self.name = kwargs.get('name', '')
        self.cities: List['City'] = kwargs.get('cities', [])
        
        # Validate required fields
        if not self.name:
            raise ValidationError("Name is required")
    
    def add_city(self, city: 'City') -> None:
        """
        Add a city to state's cities.
        
        Args:
            city: City object to add
        """
        if city not in self.cities:
            self.cities.append(city)
    
    @property
    def city_count(self) -> int:
        """
        Get number of cities in state.
        
        Returns:
            Number of cities
        """
        return len(self.cities)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert state to dictionary.
        
        Returns:
            Dictionary representation
        """
        result = super().to_dict()
        # Add derived attributes
        result['city_count'] = self.city_count
        # Remove relationship list
        result.pop('cities', None)
        return result
