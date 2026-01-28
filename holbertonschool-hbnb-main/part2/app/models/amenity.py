"""Amenity model for HBnB."""
import uuid
from datetime import datetime

class Amenity:
    """Amenity class representing an amenity in the system."""
    
    def __init__(self, **kwargs):
        """Initialize a new Amenity instance."""
        self.id = str(uuid.uuid4())
        self.name = kwargs.get('name', '')
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        # Set additional attributes if provided
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def update(self, data):
        """Update amenity attributes."""
        if 'name' in data:
            self.name = data['name']
        self.updated_at = datetime.now()
    
    def to_dict(self):
        """Convert amenity to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f"<Amenity {self.id}: {self.name}>"
