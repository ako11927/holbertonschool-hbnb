"""User model representing a platform user."""
import re
from typing import Optional, List
from .base_model import BaseModel
from ..exceptions import ValidationError


class User(BaseModel):
    """
    User model with email, password, and personal information.
    
    Attributes:
        email (str): User's email address
        password (str): Hashed password (not stored in plain text)
        first_name (str): User's first name
        last_name (str): User's last name
        reviews (list): Reviews written by the user
        places (list): Places owned by the user
    """
    
    def __init__(self, **kwargs):
        """
        Initialize user with validation.
        
        Args:
            **kwargs: User attributes including:
                email: Required, valid email format
                password: Required, minimum 6 characters
                first_name: Optional
                last_name: Optional
        """
        super().__init__(**kwargs)
        self._email = kwargs.get('email', '')
        self._password = kwargs.get('password', '')
        self.first_name = kwargs.get('first_name', '')
        self.last_name = kwargs.get('last_name', '')
        
        # Initialize relationships (will be populated by facade)
        self.reviews: List['Review'] = kwargs.get('reviews', [])
        self.places: List['Place'] = kwargs.get('places', [])
        
        # Validate on creation if email/password provided
        if 'email' in kwargs:
            self.email = kwargs['email']
        if 'password' in kwargs:
            self.password = kwargs['password']
    
    @property
    def email(self) -> str:
        """Get email."""
        return self._email
    
    @email.setter
    def email(self, value: str):
        """Set email with validation."""
        if not self._validate_email(value):
            raise ValidationError("Invalid email format")
        self._email = value
        self.save()
    
    @property
    def password(self) -> str:
        """Get password (always returns empty string for security)."""
        return ''  # Never return actual password
    
    @password.setter
    def password(self, value: str):
        """Set password with validation."""
        if len(value) < 6:
            raise ValidationError("Password must be at least 6 characters")
        # In a real application, you would hash the password here
        self._password = value
        self.save()
    
    def verify_password(self, password: str) -> bool:
        """
        Verify if provided password matches stored password.
        
        Args:
            password: Password to verify
            
        Returns:
            True if password matches
        """
        # In a real application, you would compare hashed passwords
        return password == self._password
    
    @property
    def full_name(self) -> str:
        """
        Get user's full name.
        
        Returns:
            Full name string
        """
        return f"{self.first_name} {self.last_name}".strip()
    
    def add_review(self, review: 'Review') -> None:
        """
        Add a review to user's reviews.
        
        Args:
            review: Review object to add
        """
        if review not in self.reviews:
            self.reviews.append(review)
    
    def add_place(self, place: 'Place') -> None:
        """
        Add a place to user's places.
        
        Args:
            place: Place object to add
        """
        if place not in self.places:
            self.places.append(place)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert user to dictionary, excluding password.
        
        Returns:
            Dictionary representation without password
        """
        result = super().to_dict()
        # Remove private attributes
        result.pop('_password', None)
        result.pop('_email', None)
        # Add derived attributes
        result['full_name'] = self.full_name
        # Remove relationship lists to avoid circular references
        result.pop('reviews', None)
        result.pop('places', None)
        return result
    
    @staticmethod
    def _validate_email(email: str) -> bool:
        """
        Validate email format.
        
        Args:
            email: Email to validate
            
        Returns:
            True if email is valid
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
