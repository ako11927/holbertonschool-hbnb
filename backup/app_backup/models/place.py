"""Place model representing a rental property."""
from typing import List, Dict, Any, Optional
from decimal import Decimal
from .base_model import BaseModel
from ..exceptions import ValidationError


class Place(BaseModel):
    """
    Place model representing a rental property.
    
    Attributes:
        user_id (str): ID of the user who owns the place
        name (str): Name of the place
        description (str): Description of the place
        number_rooms (int): Number of rooms
        number_bathrooms (int): Number of bathrooms
        max_guest (int): Maximum number of guests
        price_by_night (Decimal): Price per night
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
        city_id (str): ID of the city
        amenity_ids (list): List of amenity IDs
    """
    
    def __init__(self, **kwargs):
        """
        Initialize place with validation.
        
        Args:
            **kwargs: Place attributes
        """
        super().__init__(**kwargs)
        self.user_id = kwargs.get('user_id', '')
        self.name = kwargs.get('name', '')
        self.description = kwargs.get('description', '')
        self.number_rooms = kwargs.get('number_rooms', 0)
        self.number_bathrooms = kwargs.get('number_bathrooms', 0)
        self.max_guest = kwargs.get('max_guest', 0)
        
        # Handle price as Decimal
        price = kwargs.get('price_by_night', 0)
        self.price_by_night = Decimal(str(price))
        
        # Handle coordinates with validation
        self.latitude = kwargs.get('latitude', 0.0)
        self.longitude = kwargs.get('longitude', 0.0)
        
        self.city_id = kwargs.get('city_id', '')
        self.amenity_ids = kwargs.get('amenity_ids', [])
        
        # Initialize relationships
        self.reviews: List['Review'] = kwargs.get('reviews', [])
        self.amenities: List['Amenity'] = kwargs.get('amenities', [])
        
        # Validate numeric fields
        if self.number_rooms < 0:
            raise ValidationError("Number of rooms cannot be negative")
        if self.number_bathrooms < 0:
            raise ValidationError("Number of bathrooms cannot be negative")
        if self.max_guest < 0:
            raise ValidationError("Max guests cannot be negative")
        if self.price_by_night < 0:
            raise ValidationError("Price cannot be negative")
    
    @property
    def latitude(self) -> float:
        """Get latitude."""
        return self._latitude
    
    @latitude.setter
    def latitude(self, value: float):
        """Set latitude with validation."""
        if not -90 <= value <= 90:
            raise ValidationError("Latitude must be between -90 and 90")
        self._latitude = float(value)
        self.save()
    
    @property
    def longitude(self) -> float:
        """Get longitude."""
        return self._longitude
    
    @longitude.setter
    def longitude(self, value: float):
        """Set longitude with validation."""
        if not -180 <= value <= 180:
            raise ValidationError("Longitude must be between -180 and 180")
        self._longitude = float(value)
        self.save()
    
    def add_review(self, review: 'Review') -> None:
        """
        Add a review to place's reviews.
        
        Args:
            review: Review object to add
        """
        if review not in self.reviews:
            self.reviews.append(review)
    
    def add_amenity(self, amenity: 'Amenity') -> None:
        """
        Add an amenity to place's amenities.
        
        Args:
            amenity: Amenity object to add
        """
        if amenity.id not in self.amenity_ids:
            self.amenity_ids.append(amenity.id)
            self.amenities.append(amenity)
    
    def remove_amenity(self, amenity_id: str) -> bool:
        """
        Remove an amenity from place's amenities.
        
        Args:
            amenity_id: ID of amenity to remove
            
        Returns:
            True if amenity was removed
        """
        if amenity_id in self.amenity_ids:
            self.amenity_ids.remove(amenity_id)
            self.amenities = [a for a in self.amenities if a.id != amenity_id]
            self.save()
            return True
        return False
    
    @property
    def average_rating(self) -> Optional[float]:
        """
        Calculate average rating from reviews.
        
        Returns:
            Average rating or None if no reviews
        """
        if not self.reviews:
            return None
        
        total_rating = sum(review.rating for review in self.reviews)
        return total_rating / len(self.reviews)
    
    def is_available(self, check_in: str, check_out: str) -> bool:
        """
        Check if place is available for given dates.
        
        Args:
            check_in: Check-in date (ISO format)
            check_out: Check-out date (ISO format)
            
        Returns:
            True if available (simplified logic for now)
        """
        # Simplified availability check
        # In a real implementation, you would check against bookings
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert place to dictionary.
        
        Returns:
            Dictionary representation
        """
        result = super().to_dict()
        # Convert Decimal to string for JSON serialization
        result['price_by_night'] = str(self.price_by_night)
        # Add derived attributes
        result['average_rating'] = self.average_rating
        # Remove relationship lists
        result.pop('reviews', None)
        result.pop('amenities', None)
        return result
