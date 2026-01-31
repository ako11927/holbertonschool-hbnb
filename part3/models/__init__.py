"""Models package"""
try:
    from .user import User
    from .place import Place
    from .amenity import Amenity
    from .review import Review
    
    __all__ = ['User', 'Place', 'Amenity', 'Review']
    
except ImportError as e:
    print(f"Warning: Could not import models: {e}")
    # Define empty classes to avoid import errors
    class User: pass
    class Place: pass
    class Amenity: pass
    class Review: pass
