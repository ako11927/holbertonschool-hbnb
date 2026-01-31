"""Place controller for handling place-related API requests."""
from flask import request, jsonify
from app.services.place_service import PlaceService


class PlaceController:
    """Controller for place endpoints."""
    
    def __init__(self):
        """Initialize controller with service."""
        self.place_service = PlaceService()
    
    def get_places(self):
        """Get all places."""
        places, status_code = self.place_service.get_all_places()
        return jsonify(places), status_code
    
    def get_place(self, place_id):
        """Get a specific place."""
        result, status_code = self.place_service.get_place(place_id)
        return jsonify(result), status_code
    
    def create_place(self):
        """Create a new place."""
        place_data = request.get_json()
        
        if not place_data:
            return jsonify({'error': 'No input data provided'}), 400
        
        result, status_code = self.place_service.create_place(place_data)
        return jsonify(result), status_code
    
    def update_place(self, place_id):
        """Update a place."""
        place_data = request.get_json()
        
        if not place_data:
            return jsonify({'error': 'No input data provided'}), 400
        
        result, status_code = self.place_service.update_place(place_id, place_data)
        return jsonify(result), status_code
    
    def delete_place(self, place_id):
        """Delete a place."""
        result, status_code = self.place_service.delete_place(place_id)
        return jsonify(result), status_code
    
    def search_places(self):
        """Search places by title or description."""
        search_term = request.args.get('q', '')
        if not search_term:
            return jsonify({'error': 'Search term is required'}), 400
        
        places, status_code = self.place_service.search_places(search_term)
        return jsonify(places), status_code
    
    def get_places_by_city(self):
        """Get places by city."""
        city = request.args.get('city', '')
        if not city:
            return jsonify({'error': 'City is required'}), 400
        
        places, status_code = self.place_service.get_places_by_city(city)
        return jsonify(places), status_code
    
    def get_places_by_price_range(self):
        """Get places by price range."""
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        
        if not min_price or not max_price:
            return jsonify({'error': 'Both min_price and max_price are required'}), 400
        
        places, status_code = self.place_service.get_places_by_price_range(min_price, max_price)
        return jsonify(places), status_code
    
    def get_places_with_filters(self):
        """Get places with filters."""
        filters = {}
        
        # Extract filter parameters
        city = request.args.get('city')
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        min_bedrooms = request.args.get('min_bedrooms')
        min_bathrooms = request.args.get('min_bathrooms')
        min_guests = request.args.get('min_guests')
        
        if city:
            filters['city'] = city
        if min_price:
            try:
                filters['min_price'] = float(min_price)
            except ValueError:
                return jsonify({'error': 'min_price must be a number'}), 400
        if max_price:
            try:
                filters['max_price'] = float(max_price)
            except ValueError:
                return jsonify({'error': 'max_price must be a number'}), 400
        if min_bedrooms:
            try:
                filters['min_bedrooms'] = int(min_bedrooms)
            except ValueError:
                return jsonify({'error': 'min_bedrooms must be an integer'}), 400
        if min_bathrooms:
            try:
                filters['min_bathrooms'] = int(min_bathrooms)
            except ValueError:
                return jsonify({'error': 'min_bathrooms must be an integer'}), 400
        if min_guests:
            try:
                filters['min_guests'] = int(min_guests)
            except ValueError:
                return jsonify({'error': 'min_guests must be an integer'}), 400
        
        places, status_code = self.place_service.get_places_with_filters(filters)
        return jsonify(places), status_code
