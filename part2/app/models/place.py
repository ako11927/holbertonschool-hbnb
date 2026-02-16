"""Place model for HBnB."""
import uuid
from datetime import datetime

class Place:
    """Place class representing a place in the system."""
    
    def __init__(self, **kwargs):
        """Initialize a new Place instance."""
        self.id = str(uuid.uuid4())
        self.name = kwargs.get('name', '')
        self.description = kwargs.get('description', '')
        self.price_per_night = kwargs.get('price_per_night', 0.0)
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        # Set additional attributes if provided
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def update(self, data):
        """Update the  place attributes."""
        updatable_fields = ['name', 'description', 'price_per_night']
        for field in updatable_fields:
            if field in data:
                setattr(self, field, data[field])
        self.updated_at = datetime.now()
    
    def to_dict(self):
        """Convert place to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price_per_night': self.price_per_night,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f"<Place {self.id}: {self.name}>"
