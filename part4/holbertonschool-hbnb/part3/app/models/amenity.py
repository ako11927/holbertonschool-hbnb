"""Amenity model with relationships."""
from app import db
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates
from app.models import place_amenities  # Import association table


class Amenity(BaseModel):
    """Amenity model representing a property amenity."""
    __tablename__ = 'amenities'
    
    # Core attribute
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    # Relationships
    # Many-to-Many: Amenity <-> Places (an amenity can be in many places)
    places = db.relationship('Place', secondary=place_amenities,
                           back_populates='amenities', lazy=True)
    
    @validates('name')
    def validate_name(self, key, name):
        """Validate amenity name."""
        if not name or not name.strip():
            raise ValueError("Amenity name is required")
        if len(name.strip()) < 2:
            raise ValueError("Amenity name must be at least 2 characters")
        return name.strip()
    
    def to_dict(self):
        """Convert amenity object to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_with_relationships(self):
        """Convert amenity object to dictionary with relationships."""
        result = self.to_dict()
        result['places_count'] = len(self.places) if self.places else 0
        return result
    
    def __repr__(self):
        return f'<Amenity {self.name}>'
