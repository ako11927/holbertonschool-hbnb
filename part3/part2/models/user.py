import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
