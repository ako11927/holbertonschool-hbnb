"""Base model for all entities."""
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

class BaseModel:
    """Base class for all models with common attributes and methods."""
    
    def __init__(self, **kwargs):
        """
        Initialize base model.
        
        Args:
            **kwargs: Model attributes to set
        """
        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.created_at = kwargs.get('created_at', datetime.now())
        self.updated_at = kwargs.get('updated_at', datetime.now())
        
        # Set additional attributes from kwargs
        for key, value in kwargs.items():
            if key not in ['id', 'created_at', 'updated_at', '__class__']:
                setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model to dictionary.
        
        Returns:
            Dictionary representation of the model
        """
        result = {}
        for key, value in self.__dict__.items():
            if key in ['created_at', 'updated_at']:
                result[key] = value.isoformat()
            elif not key.startswith('_'):
                result[key] = value
        result['__class__'] = self.__class__.__name__
        return result
    
    def save(self) -> 'BaseModel':
        """
        Update the updated_at timestamp.
        
        Returns:
            Self for method chaining
        """
        self.updated_at = datetime.now()
        return self
    
    def update(self, **kwargs) -> 'BaseModel':
        """
        Update model attributes.
        
        Args:
            **kwargs: Attributes to update
            
        Returns:
            Self for method chaining
        """
        for key, value in kwargs.items():
            if key not in ['id', 'created_at', '__class__']:
                setattr(self, key, value)
        self.save()
        return self
    
    def __str__(self) -> str:
        """
        String representation of the model.
        
        Returns:
            String representation
        """
        class_name = self.__class__.__name__
        return f"[{class_name}] ({self.id}) {self.__dict__}"
    
    def __repr__(self) -> str:
        """
        Official string representation.
        
        Returns:
            String representation
        """
        return self.__str__()
    
    def __eq__(self, other) -> bool:
        """
        Check equality based on ID.
        
        Args:
            other: Other object to compare
            
        Returns:
            True if objects have same ID
        """
        if isinstance(other, BaseModel):
            return self.id == other.id
        return False
    
    def __hash__(self) -> int:
        """
        Hash based on ID.
        
        Returns:
            Hash value
        """
        return hash(self.id)
