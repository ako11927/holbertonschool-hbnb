#!/usr/bin/python3
"""
Enhanced BaseModel for HBNB
"""
import uuid
from datetime import datetime
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
import hashlib
import json

Base = declarative_base()


class BaseModel:
    """
    Enhanced BaseModel class with validation, serialization improvements,
    and soft delete support
    """
    
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow,
                       onupdate=datetime.utcnow)
    is_active = Column(String(1), default='1', nullable=False)  # Soft delete flag
    
    def __init__(self, *args, **kwargs):
        """
        Enhanced initialization with validation and hash generation
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                self.created_at = datetime.now()
            if 'updated_at' not in kwargs:
                self.updated_at = datetime.now()
            if 'is_active' not in kwargs:
                self.is_active = '1'
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()
            self.is_active = '1'
        
        # Generate object hash for change detection
        self.__generate_hash()
    
    def __generate_hash(self):
        """
        Generate hash for change detection
        """
        data = {k: str(v) for k, v in self.__dict__.items() 
                if not k.startswith('_') and k != 'hash'}
        data_str = json.dumps(data, sort_keys=True)
        self._hash = hashlib.md5(data_str.encode()).hexdigest()
    
    def save(self):
        """
        Enhanced save method with change detection and audit logging
        """
        old_hash = getattr(self, '_hash', None)
        self.__generate_hash()
        
        # Only update if changes detected
        if old_hash != self._hash:
            self.updated_at = datetime.now()
            models.storage.new(self)
            models.storage.save()
            
            # Log change if in development
            if models.storage.__class__.__name__ == 'DBStorage':
                self._log_change()
    
    def to_dict(self):
        """
        Enhanced dictionary representation with computed fields
        """
        obj_dict = self.__dict__.copy()
        
        # Remove SQLAlchemy internal attributes
        obj_dict.pop('_sa_instance_state', None)
        
        # Convert datetime to string
        for key in ['created_at', 'updated_at']:
            if key in obj_dict and obj_dict[key]:
                if isinstance(obj_dict[key], datetime):
                    obj_dict[key] = obj_dict[key].isoformat()
        
        # Add class name
        obj_dict['__class__'] = self.__class__.__name__
        
        # Add computed fields
        obj_dict['_hash'] = self._hash
        obj_dict['is_active'] = self.is_active
        
        return obj_dict
    
    def delete(self, soft=True):
        """
        Enhanced delete with soft delete option
        """
        if soft:
            self.is_active = '0'
            self.save()
        else:
            models.storage.delete(self)
            models.storage.save()
    
    def restore(self):
        """
        Restore soft-deleted object
        """
        self.is_active = '1'
        self.save()
    
    def validate(self):
        """
        Validate object data
        """
        errors = {}
        
        # ID validation
        if not self.id or len(self.id) != 36:
            errors['id'] = 'Invalid UUID'
        
        # Timestamp validation
        if self.created_at > datetime.now():
            errors['created_at'] = 'Creation date cannot be in the future'
        
        if self.updated_at < self.created_at:
            errors['updated_at'] = 'Update date cannot be before creation date'
        
        # Custom validation hook
        self._custom_validation(errors)
        
        return errors
    
    def _custom_validation(self, errors):
        """
        Hook for subclasses to add custom validation
        """
        pass
    
    def __str__(self):
        """
        Enhanced string representation
        """
        status = "Active" if self.is_active == '1' else "Inactive"
        return f"[{self.__class__.__name__}] ({self.id}) {status} - {self.__dict__}"
    
    def _log_change(self):
        """
        Log changes for audit trail (development only)
        """
        import os
        if os.getenv('HBNB_ENV') == 'development':
            print(f"[AUDIT] {self.__class__.__name__} {self.id} updated at {datetime.now()}")
