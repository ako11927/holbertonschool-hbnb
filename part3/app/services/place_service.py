"""Place service for business logic."""
from app.services.facade import HBnBFacade


class PlaceService:
    """Service for place operations."""
    
    def __init__(self):
        """Initialize service with facade."""
        self.facade = HBnBFacade()
    
    def create_place(self, place_data):
        """Create a new place."""
        try:
            # Validate required fields
            required_fields = ['title', 'description', 'price']
            for field in required_fields:
                if not place_data.get(field):
                    return {'error': f'{field} is required'}, 400
            
            # Create place via facade
            place = self.facade.create_place(place_data)
            return place.to_dict(), 201
        
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Failed to create place'}, 500
    
    def get_place(self, place_id):
        """Get a place by ID."""
        place = self.facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict(), 200
    
    def get_all_places(self):
        """Get all places."""
        places = self.facade.get_all_places()
        return [place.to_dict() for place in places], 200
    
    def update_place(self, place_id, place_data):
        """Update a place."""
        try:
            place = self.facade.update_place(place_id, place_data)
            if not place:
                return {'error': 'Place not found'}, 404
            return place.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
    
    def delete_place(self, place_id):
        """Delete a place."""
        success = self.facade.delete_place(place_id)
        if not success:
            return {'error': 'Place not found'}, 404
        return {'message': 'Place deleted successfully'}, 200
    
    def search_places(self, search_term):
        """Search places by title or description."""
        places = self.facade.search_places(search_term)
        return [place.to_dict() for place in places], 200
    
    def get_places_by_city(self, city):
        """Get all places in a city."""
        places = self.facade.get_places_by_city(city)
        return [place.to_dict() for place in places], 200
    
    def get_places_by_price_range(self, min_price, max_price):
        """Get places within a price range."""
        try:
            min_price_float = float(min_price)
            max_price_float = float(max_price)
            places = self.facade.get_places_by_price_range(min_price_float, max_price_float)
            return [place.to_dict() for place in places], 200
        except (ValueError, TypeError):
            return {'error': 'Invalid price range'}, 400
    
    def get_places_with_filters(self, filters):
        """Get places with various filters."""
        places = self.facade.get_places_with_filters(filters)
        return [place.to_dict() for place in places], 200
