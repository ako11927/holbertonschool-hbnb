"""Place repository for database operations with relationships."""
from app import db
from app.models.place import Place
from app.repositories.base_repository import BaseRepository


class PlaceRepository(BaseRepository):
    """Repository for Place model operations with relationships."""
    
    def __init__(self):
        """Initialize PlaceRepository with Place model."""
        super().__init__(Place)
    
    def create_place(self, place_data):
        """Create a new place with owner relationship."""
        # Create place instance
        place = Place(
            title=place_data['title'],
            description=place_data['description'],
            price=place_data['price'],
            address=place_data.get('address', ''),
            city=place_data.get('city', ''),
            max_guests=place_data.get('max_guests', 1),
            bedrooms=place_data.get('bedrooms', 1),
            bathrooms=place_data.get('bathrooms', 1),
            owner_id=place_data['owner_id']  # Required for relationship
        )
        
        # Handle optional coordinates
        if 'latitude' in place_data:
            place.latitude = place_data['latitude']
        if 'longitude' in place_data:
            place.longitude = place_data['longitude']
        
        # Handle amenities if provided
        if 'amenities' in place_data:
            from app.repositories.amenity_repository import AmenityRepository
            amenity_repo = AmenityRepository()
            for amenity_id in place_data['amenities']:
                amenity = amenity_repo.get(amenity_id)
                if amenity:
                    place.amenities.append(amenity)
        
        # Save to database
        db.session.add(place)
        db.session.commit()
        return place
    
    def get_place_with_relationships(self, place_id):
        """Get a place with all relationships loaded."""
        from sqlalchemy.orm import joinedload
        place = self.model.query.options(
            joinedload(Place.owner),
            joinedload(Place.reviews),
            joinedload(Place.amenities)
        ).get(place_id)
        return place
    
    def get_places_by_owner(self, owner_id):
        """Get all places owned by a user."""
        return self.model.query.filter_by(owner_id=owner_id).all()
    
    def get_places_by_city(self, city):
        """Get all places in a specific city."""
        return self.model.query.filter_by(city=city).all()
    
    def search_places(self, search_term):
        """Search places by title or description."""
        return self.model.query.filter(
            (Place.title.ilike(f'%{search_term}%')) | 
            (Place.description.ilike(f'%{search_term}%'))
        ).all()
    
    def get_places_by_price_range(self, min_price, max_price):
        """Get places within a price range."""
        return self.model.query.filter(
            Place.price >= min_price,
            Place.price <= max_price
        ).all()
    
    def get_places_with_filters(self, filters):
        """Get places with various filters."""
        query = self.model.query
        
        if 'city' in filters:
            query = query.filter_by(city=filters['city'])
        if 'min_price' in filters:
            query = query.filter(Place.price >= filters['min_price'])
        if 'max_price' in filters:
            query = query.filter(Place.price <= filters['max_price'])
        if 'min_bedrooms' in filters:
            query = query.filter(Place.bedrooms >= filters['min_bedrooms'])
        if 'min_bathrooms' in filters:
            query = query.filter(Place.bathrooms >= filters['min_bathrooms'])
        if 'min_guests' in filters:
            query = query.filter(Place.max_guests >= filters['min_guests'])
        
        return query.all()
    
    def add_amenity_to_place(self, place_id, amenity_id):
        """Add an amenity to a place."""
        place = self.get(place_id)
        if not place:
            return None
        
        from app.repositories.amenity_repository import AmenityRepository
        amenity_repo = AmenityRepository()
        amenity = amenity_repo.get(amenity_id)
        
        if not amenity:
            return None
        
        if amenity not in place.amenities:
            place.amenities.append(amenity)
            db.session.commit()
        
        return place
    
    def remove_amenity_from_place(self, place_id, amenity_id):
        """Remove an amenity from a place."""
        place = self.get(place_id)
        if not place:
            return None
        
        from app.repositories.amenity_repository import AmenityRepository
        amenity_repo = AmenityRepository()
        amenity = amenity_repo.get(amenity_id)
        
        if not amenity:
            return None
        
        if amenity in place.amenities:
            place.amenities.remove(amenity)
            db.session.commit()
        
        return place
    
    def get_place_reviews(self, place_id):
        """Get all reviews for a place."""
        place = self.get(place_id)
        if place:
            return place.reviews
        return []
