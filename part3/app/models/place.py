"""Place model with relationships."""
from app import db
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates
from app.models import place_amenities  # Import association table


class Place(BaseModel):
    """Place model representing a rental property."""
    __tablename__ = 'places'
    
    # Core attributes
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    max_guests = db.Column(db.Integer, default=1)
    bedrooms = db.Column(db.Integer, default=1)
    bathrooms = db.Column(db.Integer, default=1)
    
    # Foreign Keys
    # One-to-Many: User -> Places (a place belongs to one user)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    # Many-to-One: Place -> User (a place has one owner)
    owner = db.relationship('User', back_populates='places')
    
    # One-to-Many: Place -> Reviews (a place can have many reviews)
    reviews = db.relationship('Review', back_populates='place',
                            cascade='all, delete-orphan', lazy=True)
    
    # Many-to-Many: Place <-> Amenities (a place can have many amenities)
    amenities = db.relationship('Amenity', secondary=place_amenities,
                              back_populates='places', lazy=True)
    
    @validates('title')
    def validate_title(self, key, title):
        """Validate place title."""
        if not title or not title.strip():
            raise ValueError("Title is required")
        if len(title.strip()) < 3:
            raise ValueError("Title must be at least 3 characters")
        return title.strip()
    
    @validates('description')
    def validate_description(self, key, description):
        """Validate place description."""
        if not description or not description.strip():
            raise ValueError("Description is required")
        if len(description.strip()) < 10:
            raise ValueError("Description must be at least 10 characters")
        return description.strip()
    
    @validates('price')
    def validate_price(self, key, price):
        """Validate price."""
        if price is None:
            raise ValueError("Price is required")
        try:
            price_float = float(price)
            if price_float <= 0:
                raise ValueError("Price must be positive")
            return price_float
        except (ValueError, TypeError):
            raise ValueError("Price must be a valid number")
    
    @validates('latitude', 'longitude')
    def validate_coordinates(self, key, coordinate):
        """Validate latitude and longitude."""
        if coordinate is not None:
            try:
                coord_float = float(coordinate)
                if key == 'latitude' and (coord_float < -90 or coord_float > 90):
                    raise ValueError("Latitude must be between -90 and 90")
                if key == 'longitude' and (coord_float < -180 or coord_float > 180):
                    raise ValueError("Longitude must be between -180 and 180")
                return coord_float
            except (ValueError, TypeError):
                raise ValueError(f"{key} must be a valid number")
        return None
    
    @validates('max_guests', 'bedrooms', 'bathrooms')
    def validate_counts(self, key, count):
        """Validate counts for guests, bedrooms, and bathrooms."""
        if count is None:
            if key == 'max_guests':
                return 1
            return 0
        
        try:
            count_int = int(count)
            if count_int < 0:
                raise ValueError(f"{key.replace('_', ' ')} cannot be negative")
            return count_int
        except (ValueError, TypeError):
            raise ValueError(f"{key.replace('_', ' ')} must be a valid integer")
    
    def to_dict(self):
        """Convert place object to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.address,
            'city': self.city,
            'max_guests': self.max_guests,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'owner_id': self.owner_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_with_relationships(self):
        """Convert place object to dictionary with relationships."""
        result = self.to_dict()
        
        # Include owner information
        if self.owner:
            result['owner'] = self.owner.to_dict_without_email()
        
        # Include reviews
        result['reviews'] = [review.to_dict() for review in self.reviews]
        result['reviews_count'] = len(self.reviews)
        
        # Include amenities
        result['amenities'] = [amenity.to_dict() for amenity in self.amenities]
        result['amenities_count'] = len(self.amenities)
        
        # Calculate average rating
        if self.reviews:
            total_rating = sum(review.rating for review in self.reviews)
            result['average_rating'] = round(total_rating / len(self.reviews), 1)
        else:
            result['average_rating'] = 0.0
        
        return result
    
    def add_amenity(self, amenity):
        """Add an amenity to this place."""
        if amenity not in self.amenities:
            self.amenities.append(amenity)
            return True
        return False
    
    def remove_amenity(self, amenity):
        """Remove an amenity from this place."""
        if amenity in self.amenities:
            self.amenities.remove(amenity)
            return True
        return False
    
    def __repr__(self):
        return f'<Place {self.title}>'
