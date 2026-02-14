"""Amenity repository for database operations."""
from app.models.amenity import Amenity
from app.repositories.base_repository import BaseRepository


class AmenityRepository(BaseRepository):
    """Repository for Amenity model operations."""
    
    def __init__(self):
        """Initialize AmenityRepository with Amenity model."""
        super().__init__(Amenity)
    
    def create_amenity(self, amenity_data):
        """Create a new amenity."""
        # Check if amenity already exists
        existing_amenity = self.get_amenity_by_name(amenity_data['name'])
        if existing_amenity:
            raise ValueError("Amenity with this name already exists")
        
        # Create amenity instance
        amenity = Amenity(name=amenity_data['name'])
        
        # Save to database
        return self.add(amenity)
    
    def get_amenity_by_name(self, name):
        """Get amenity by name."""
        return self.model.query.filter_by(name=name).first()
    
    def search_amenities(self, search_term):
        """Search amenities by name."""
        return self.model.query.filter(Amenity.name.ilike(f'%{search_term}%')).all()
