"""Custom exceptions for HBnB."""

class HBnBError(Exception):
    """Base exception for HBnB errors."""
    pass

class NotFoundError(HBnBError):
    """Raised when a resource is not found."""
    pass

class ValidationError(HBnBError):
    """Raised when input validation fails."""
    pass

class DuplicateError(HBnBError):
    """Raised when a duplicate resource is detected."""
    pass
