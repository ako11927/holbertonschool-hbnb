from app import db
from .base_model import BaseModel

# Association table for Many-to-Many relationship between Place and Amenity
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Amenity(BaseModel):
    """SQLAlchemy model representing an amenity."""
    
    __tablename__ = 'amenities'

    # Core attribute
    name = db.Column(db.String(100), nullable=False, unique=True)

    # ========== Relationships ==========
    places = db.relationship(
        'Place',
        secondary=place_amenity,
        lazy='subquery',
        backref=db.backref('amenities', lazy=True)
    )

    # ========== Methods ==========
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.name:
            raise ValueError("name is required")

    def update(self, data):
        """Update Amenity attributes."""
        if 'name' in data:
            self.name = data['name']
        self.save()

    def to_dict(self):
        """Convert Amenity to dictionary representation."""
        result = super().to_dict()
        result.update({
            'name': self.name,
            # Optionally include IDs of associated places
            'place_ids': [place.id for place in self.places]
        })
        return result

    def __repr__(self):
        return f"<Amenity {self.id}: {self.name}>"
