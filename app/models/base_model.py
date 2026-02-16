"""Base model for all SQLAlchemy entities."""
import uuid
from datetime import datetime
from app import db

class BaseModel(db.Model):
    """Base class for all models with common attributes and methods."""
    
    __abstract__ = True  # لا يتم إنشاء جدول لهذه الكلاس مباشرة

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self) -> dict:
        """
        Convert model to dictionary.
        Returns:
            Dictionary representation of the model
        """
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            else:
                result[column.name] = value
        result['__class__'] = self.__class__.__name__
        return result

    def save(self):
        """
        Add or update model in the database.
        """
        from app import db
        db.session.add(self)
        db.session.commit()
        return self

    def update(self, **kwargs):
        """
        Update model attributes and save to database.
        """
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ['id', 'created_at']:
                setattr(self, key, value)
        self.save()
        return self

    def __str__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.to_dict()}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, BaseModel):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)
