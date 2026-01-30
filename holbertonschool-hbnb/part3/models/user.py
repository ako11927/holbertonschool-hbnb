import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    password_hash: str = ""
    is_admin: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def update(self, data: dict) -> None:
        """Update user attributes. Allowed: first_name, last_name, email, password_hash, is_admin."""
        allowed = {'first_name', 'last_name', 'email', 'password_hash', 'is_admin'}
        for k, v in data.items():
            if k in allowed and hasattr(self, k):
                setattr(self, k, v)
        self.updated_at = datetime.now()

    def to_dict(self):
        """Convert to dict; never expose password_hash."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
