from app import db
from .base_model import BaseModel

# Association table for many-to-many: Place ↔ Amenity
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    """Place model representing a place in the system."""

    __tablename__ = 'places'

    # Core attributes
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price_per_night = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # ========== Relationships ==========
    # One-to-Many: Place → Review
    reviews = db.relationship('Review', backref='place', lazy=True)

    # Many-to-One: Place → User
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Many-to-Many: Place ↔ Amenity
    amenities = db.relationship(
        'Amenity',
        secondary=place_amenity,
        lazy='subquery',
        backref=db.backref('places', lazy=True)
    )

    # ========== Methods ==========
    def update(self, data):
        """Update place attributes."""
        updatable_fields = ['name', 'description', 'price_per_night', 'latitude', 'longitude', 'user_id']
        for field in updatable_fields:
            if field in data:
                setattr(self, field, data[field])
