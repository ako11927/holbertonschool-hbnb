"""In-memory repository implementation."""
from typing import Dict, Any, Optional, List
from persistence.base_repository import BaseRepository

class InMemoryRepository(BaseRepository):
    """In-memory repository for object storage."""
    
    def __init__(self):
        """Initialize the repository."""
        self._storage: Dict[str, Any] = {}
    
    def create(self, obj) -> Any:
        """Create a new object in storage."""
        if not hasattr(obj, 'id'):
            raise ValueError("Object must have an 'id' attribute")
        
        if obj.id in self._storage:
            raise ValueError(f"Object with id {obj.id} already exists")
        
        self._storage[obj.id] = obj
        return obj
    
    def get(self, obj_id: str) -> Optional[Any]:
        """Get an object by ID."""
        return self._storage.get(obj_id)
    
    def update(self, obj_id: str, obj_data: Dict[str, Any]) -> Optional[Any]:
        """Update an existing object."""
        if obj_id not in self._storage:
            return None
        
        obj = self._storage[obj_id]
        
        # Update object attributes
        for key, value in obj_data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        
        # Call save method if it exists
        if hasattr(obj, 'save'):
            obj.save()
        
        return obj
    
    def delete(self, obj_id: str) -> bool:
        """Delete an object by ID."""
        if obj_id in self._storage:
            del self._storage[obj_id]
            return True
        return False
    
    def get_all(self) -> List[Any]:
        """Get all objects."""
        return list(self._storage.values())
    
    def find_by(self, **kwargs) -> List[Any]:
        """Find objects by attributes."""
        results = []
        for obj in self._storage.values():
            match = True
            for key, value in kwargs.items():
                if not hasattr(obj, key) or getattr(obj, key) != value:
                    match = False
                    break
            if match:
                results.append(obj)
        return results
    
    def clear(self):
        """Clear all objects from storage."""
        self._storage.clear()
    
    def count(self) -> int:
        """Get the count of objects in storage."""
        return len(self._storage)
