"""Amenity controller for handling amenity-related API requests."""
from flask import request, jsonify
from app.services.amenity_service import AmenityService


class AmenityController:
    """Controller for amenity endpoints."""
    
    def __init__(self):
        """Initialize controller with service."""
        self.amenity_service = AmenityService()
    
    def get_amenities(self):
        """Get all amenities."""
        amenities, status_code = self.amenity_service.get_all_amenities()
        return jsonify(amenities), status_code
    
    def get_amenity(self, amenity_id):
        """Get a specific amenity."""
        result, status_code = self.amenity_service.get_amenity(amenity_id)
        return jsonify(result), status_code
    
    def create_amenity(self):
        """Create a new amenity."""
        amenity_data = request.get_json()
        
        if not amenity_data:
            return jsonify({'error': 'No input data provided'}), 400
        
        result, status_code = self.amenity_service.create_amenity(amenity_data)
        return jsonify(result), status_code
    
    def update_amenity(self, amenity_id):
        """Update an amenity."""
        amenity_data = request.get_json()
        
        if not amenity_data:
            return jsonify({'error': 'No input data provided'}), 400
        
        result, status_code = self.amenity_service.update_amenity(amenity_id, amenity_data)
        return jsonify(result), status_code
    
    def delete_amenity(self, amenity_id):
        """Delete an amenity."""
        result, status_code = self.amenity_service.delete_amenity(amenity_id)
        return jsonify(result), status_code
    
    def search_amenities(self):
        """Search amenities by name."""
        search_term = request.args.get('q', '')
        if not search_term:
            return jsonify({'error': 'Search term is required'}), 400
        
        amenities, status_code = self.amenity_service.search_amenities(search_term)
        return jsonify(amenities), status_code
