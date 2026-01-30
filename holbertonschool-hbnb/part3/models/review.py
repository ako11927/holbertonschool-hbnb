import uuid
from typing import Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Review:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    text: str = ""
    rating: int = 0
    user_id: str = ""
    place_id: str = ""
    user: Optional['User'] = None
    place: Optional['Place'] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        review_dict = {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if self.user:
            review_dict['user'] = {
                'id': self.user.id,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'email': self.user.email
            }
        
        if self.place:
            review_dict['place'] = {
                'id': self.place.id,
                'title': self.place.title
            }
        
        return review_dict
