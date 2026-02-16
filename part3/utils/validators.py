"""Enhanced validation utilities."""
import re
from decimal import Decimal
from typing import Dict, Any, Tuple

def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email format.
    
    Args:
        email: Email to validate
        
    Returns:
        Tuple of (is_valid, message)
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"
    return True, "Email is valid"

def validate_password(password: str) -> Tuple[bool, str]:
    """
    Validate password strength.
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, message)
    """
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one digit"
    
    if not any(char.isalpha() for char in password):
        return False, "Password must contain at least one letter"
    
    return True, "Password is valid"

def validate_rating(rating: int) -> Tuple[bool, str]:
    """
    Validate rating value.
    
    Args:
        rating: Rating to validate
        
    Returns:
        Tuple of (is_valid, message)
    """
    if not isinstance(rating, int):
        return False, "Rating must be an integer"
    
    if rating < 1 or rating > 5:
        return False, "Rating must be between 1 and 5"
    
    return True, "Rating is valid"

def validate_coordinates(latitude: float, longitude: float) -> Tuple[bool, str]:
    """
    Validate geographic coordinates.
    
    Args:
        latitude: Latitude value
        longitude: Longitude value
        
    Returns:
        Tuple of (is_valid, message)
    """
    if latitude < -90 or latitude > 90:
        return False, "Latitude must be between -90 and 90"
    
    if longitude < -180 or longitude > 180:
        return False, "Longitude must be between -180 and 180"
    
    return True, "Coordinates are valid"

def validate_price(price: Any) -> Tuple[bool, str, Decimal]:
    """
    Validate price and convert to Decimal.
    
    Args:
        price: Price value
        
    Returns:
        Tuple of (is_valid, message, decimal_price)
    """
    try:
        decimal_price = Decimal(str(price))
        if decimal_price < 0:
            return False, "Price cannot be negative", decimal_price
        return True, "Price is valid", decimal_price
    except Exception:
        return False, "Invalid price format", Decimal('0')

def validate_required_fields(data: Dict[str, Any], required_fields: list) -> Tuple[bool, str]:
    """
    Validate that all required fields are present.
    
    Args:
        data: Data dictionary
        required_fields: List of required field names
        
    Returns:
        Tuple of (is_valid, message)
    """
    missing_fields = []
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == '':
            missing_fields.append(field)
    
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    return True, "All required fields are present"

def validate_string_length(value: str, min_length: int = 0, max_length: int = None) -> Tuple[bool, str]:
    """
    Validate string length.
    
    Args:
        value: String to validate
        min_length: Minimum length
        max_length: Maximum length
        
    Returns:
        Tuple of (is_valid, message)
    """
    if len(value) < min_length:
        return False, f"Must be at least {min_length} characters"
    
    if max_length and len(value) > max_length:
        return False, f"Must be at most {max_length} characters"
    
    return True, "Length is valid"

def validate_integer_range(value: int, min_val: int = None, max_val: int = None) -> Tuple[bool, str]:
    """
    Validate integer range.
    
    Args:
        value: Integer to validate
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        Tuple of (is_valid, message)
    """
    if not isinstance(value, int):
        return False, "Must be an integer"
    
    if min_val is not None and value < min_val:
        return False, f"Must be at least {min_val}"
    
    if max_val is not None and value > max_val:
        return False, f"Must be at most {max_val}"
    
    return True, "Value is valid"
