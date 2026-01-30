import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Amenity:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def update(self, data: dict) -> None:
        """Update amenity attributes. Allowed: name."""
        if 'name' in data:
            self.name = data['name']
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
