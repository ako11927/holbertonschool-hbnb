import uuid
from typing import List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Place:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    price: float = 0.0
    latitude: float = 0.0
    longitude: float = 0.0
    owner_id: str = ""
    owner: Optional['User'] = None
    amenities: List['Amenity'] = field(default_factory=list)
    reviews: List['Review'] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        # Set private attributes directly, not through properties
        self._price = float(self.price) if hasattr(self, 'price') else 0.0
        self._latitude = float(self.latitude) if hasattr(self, 'latitude') else 0.0
        self._longitude = float(self.longitude) if hasattr(self, 'longitude') else 0.0
        
        # Run validations
        self._validate_price()
        self._validate_latitude()
        self._validate_longitude()
    
    @property
    def price(self) -> float:
        return self._price
    
    @price.setter
    def price(self, value: float):
        try:
            self._price = float(value)
        except (ValueError, TypeError):
            self._price = 0.0
        self._validate_price()
    
    @property
    def latitude(self) -> float:
        return self._latitude
    
    @latitude.setter
    def latitude(self, value: float):
        try:
            self._latitude = float(value)
        except (ValueError, TypeError):
            self._latitude = 0.0
        self._validate_latitude()
    
    @property
    def longitude(self) -> float:
        return self._longitude
    
    @longitude.setter
    def longitude(self, value: float):
        try:
            self._longitude = float(value)
        except (ValueError, TypeError):
            self._longitude = 0.0
        self._validate_longitude()
    
    def _validate_price(self):
        if hasattr(self, '_price'):
            if self._price < 0:
                raise ValueError("Price must be a non-negative number")
    
    def _validate_latitude(self):
        if hasattr(self, '_latitude'):
            if not -90 <= self._latitude <= 90:
                raise ValueError("Latitude must be between -90 and 90")
    
    def _validate_longitude(self):
        if hasattr(self, '_longitude'):
            if not -180 <= self._longitude <= 180:
                raise ValueError("Longitude must be between -180 and 180")
    
    def to_dict(self, include_related=True):
        """Convert place to dictionary"""
        place_dict = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_related:
            if self.owner:
                place_dict['owner'] = {
                    'id': self.owner.id,
                    'first_name': self.owner.first_name,
                    'last_name': self.owner.last_name,
                    'email': self.owner.email
                }
            
            place_dict['amenities'] = [
                {
                    'id': amenity.id,
                    'name': amenity.name
                }
                for amenity in self.amenities
            ]
            
            place_dict['reviews'] = [
                {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user_id
                }
                for review in self.reviews
            ]
        
        return place_dict
    
    def update(self, data: dict):
        """Update place attributes"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'owner', 'amenities', 'reviews', 'created_at']:
                setattr(self, key, value)
        self.updated_at = datetime.now()
