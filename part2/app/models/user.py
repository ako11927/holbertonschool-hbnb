"""User model for HBnB."""
import uuid
from datetime import datetime

class User:
    """User class representing a user in the system."""
    
    def __init__(self, **kwargs):
        """Initialize a new User instance."""
        self.id = str(uuid.uuid4())
        self.first_name = kwargs.get('first_name', '')
        self.last_name = kwargs.get('last_name', '')
        self.email = kwargs.get('email', '')
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        # Set additional attributes if provided
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def update(self, data):
        """Update user attributes."""
        updatable_fields = ['first_name', 'last_name', 'email']
        for field in updatable_fields:
            if field in data:
                setattr(self, field, data[field])
        self.updated_at = datetime.now()
    
    def to_dict(self):
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f"<User {self.id}: {self.first_name} {self.last_name}>"
