"""Place model for HBnB."""
import uuid
from datetime import datetime


class Place:
    """Place class representing a place in the system."""

    def __init__(self, **kwargs):
        """Initialize a new Place instance."""
        self.id = kwargs.get('id') or str(uuid.uuid4())
        self.title = kwargs.get('title', kwargs.get('name', ''))
        self.description = kwargs.get('description', '')
        self.price = float(kwargs.get('price', kwargs.get('price_per_night', 0.0)))
        self.latitude = float(kwargs.get('latitude', 0.0))
        self.longitude = float(kwargs.get('longitude', 0.0))
        self.owner_id = str(kwargs.get('owner_id', ''))
        self.created_at = kwargs.get('created_at') or datetime.now()
        self.updated_at = kwargs.get('updated_at') or datetime.now()
        self.owner = kwargs.get('owner')
        self.amenities = getattr(self, 'amenities', None) or kwargs.get('amenities') or []
        self.reviews = getattr(self, 'reviews', None) or kwargs.get('reviews') or []

    def update(self, data):
        """Update place attributes."""
        updatable_fields = [
            'title', 'name', 'description', 'price', 'price_per_night',
            'latitude', 'longitude', 'owner_id'
        ]
        for field in updatable_fields:
            if field in data:
                v = data[field]
                if field == 'price' or field == 'price_per_night':
                    setattr(self, 'price', float(v))
                elif field == 'latitude':
                    self.latitude = float(v)
                elif field == 'longitude':
                    self.longitude = float(v)
                elif field == 'title' or field == 'name':
                    self.title = v
                else:
                    setattr(self, field, v)
        self.updated_at = datetime.now()

    def to_dict(self):
        """Convert place to dictionary."""
        d = {
            'id': self.id,
            'title': getattr(self, 'title', getattr(self, 'name', '')),
            'description': self.description,
            'price': getattr(self, 'price', getattr(self, 'price_per_night', 0.0)),
            'latitude': getattr(self, 'latitude', 0.0),
            'longitude': getattr(self, 'longitude', 0.0),
            'owner_id': str(getattr(self, 'owner_id', '')),
            'created_at': self.created_at.isoformat() if hasattr(self.created_at, 'isoformat') else str(self.created_at),
            'updated_at': self.updated_at.isoformat() if hasattr(self.updated_at, 'isoformat') else str(self.updated_at),
        }
        if getattr(self, 'owner', None):
            d['owner'] = self.owner.to_dict() if hasattr(self.owner, 'to_dict') else self.owner
        if getattr(self, 'amenities', None):
            d['amenities'] = [a.to_dict() if hasattr(a, 'to_dict') else a for a in self.amenities]
        if getattr(self, 'reviews', None):
            d['reviews'] = [r.to_dict() if hasattr(r, 'to_dict') else {'id': r.id, 'text': getattr(r, 'text', ''), 'rating': getattr(r, 'rating', 0), 'user_id': getattr(r, 'user_id', '')} for r in self.reviews]
        return d

    def __repr__(self):
        return f"<Place {self.id}: {getattr(self, 'title', '')}>"
