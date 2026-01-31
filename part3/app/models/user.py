"""User model with relationships."""
from app import db, bcrypt
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates
import re


class User(BaseModel):
    """User model representing a registered user."""
    __tablename__ = 'users'
    
    # User-specific attributes
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationships
    # One-to-Many: User -> Places (a user can own many places)
    places = db.relationship('Place', back_populates='owner', 
                           cascade='all, delete-orphan', lazy=True)
    
    # One-to-Many: User -> Reviews (a user can write many reviews)
    reviews = db.relationship('Review', back_populates='user',
                            cascade='all, delete-orphan', lazy=True)
    
    @validates('email')
    def validate_email(self, key, email):
        """Validate email format."""
        if not email:
            raise ValueError("Email is required")
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError("Invalid email format")
        return email.lower()
    
    @validates('first_name', 'last_name')
    def validate_names(self, key, name):
        """Validate first and last names."""
        if not name or not name.strip():
            raise ValueError(f"{key.replace('_', ' ').title()} is required")
        if len(name.strip()) < 2:
            raise ValueError(f"{key.replace('_', ' ').title()} must be at least 2 characters")
        return name.strip()
    
    @property
    def password(self):
        """Password property - prevent password from being read."""
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        """Set password - hash it using bcrypt."""
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def verify_password(self, password):
        """Verify a password against the stored hash."""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = password
    
    def to_dict(self):
        """Convert user object to dictionary."""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_with_relationships(self):
        """Convert user object to dictionary with relationships."""
        result = self.to_dict()
        # Include basic info about relationships
        result['places_count'] = len(self.places) if self.places else 0
        result['reviews_count'] = len(self.reviews) if self.reviews else 0
        return result
    
    def to_dict_without_email(self):
        """Convert user object to dictionary without email (for public views)."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<User {self.email}>'
