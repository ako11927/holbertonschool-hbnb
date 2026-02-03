"""Association tables and model imports."""
from app import db

# Association table for many-to-many relationship between places and amenities
place_amenities = db.Table('place_amenities',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), 
              primary_key=True, nullable=False),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), 
              primary_key=True, nullable=False),
    db.Column('created_at', db.DateTime, default=db.func.current_timestamp())
)

# Import all models to ensure they're registered with SQLAlchemy
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
