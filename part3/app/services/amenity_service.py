"""Amenity service for business logic."""
from app.services.facade import HBnBFacade


class AmenityService:
    """Service for amenity operations."""
    
    def __init__(self):
        """Initialize service with facade."""
        self.facade = HBnBFacade()
    
    def create_amenity(self, amenity_data):
        """Create a new amenity."""
        try:
            # Validate required fields
            if not amenity_data.get('name'):
                return {'error': 'name is required'}, 400
            
            # Create amenity via facade
            amenity = self.facade.create_amenity(amenity_data)
            return amenity.to_dict(), 201
        
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Failed to create amenity'}, 500
    
    def get_amenity(self, amenity_id):
        """Get an amenity by ID."""
        amenity = self.facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200
    
    def get_all_amenities(self):
        """Get all amenities."""
        amenities = self.facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200
    
    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity."""
        try:
            amenity = self.facade.update_amenity(amenity_id, amenity_data)
            if not amenity:
                return {'error': 'Amenity not found'}, 404
            return amenity.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
    
    def delete_amenity(self, amenity_id):
        """Delete an amenity."""
        success = self.facade.delete_amenity(amenity_id)
        if not success:
            return {'error': 'Amenity not found'}, 404
        return {'message': 'Amenity deleted successfully'}, 200
    
    def get_amenity_by_name(self, name):
        """Get amenity by name."""
        amenity = self.facade.get_amenity_by_name(name)
        if not amenity:
            return None
        return amenity.to_dict()
    
    def search_amenities(self, search_term):
        """Search amenities by name."""
        amenities = self.facade.search_amenities(search_term)
        return [amenity.to_dict() for amenity in amenities], 200
