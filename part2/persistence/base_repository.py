"""Base repository interface."""
from abc import ABC, abstractmethod

class BaseRepository(ABC):
    """Abstract base class for repositories."""
    
    @abstractmethod
    def create(self, obj):
        """Create a new object."""
        pass
    
    @abstractmethod
    def get(self, obj_id):
        """Get an object by ID."""
        pass
    
    @abstractmethod
    def update(self, obj_id, obj_data):
        """Update an object."""
        pass
    
    @abstractmethod
    def delete(self, obj_id):
        """Delete an object."""
        pass
    
    @abstractmethod
    def get_all(self):
        """Get all objects."""
        pass
