"""Custom exceptions for business logic."""


class BusinessLogicError(Exception):
    """Base exception for business logic errors."""
    pass


class ValidationError(BusinessLogicError):
    """Raised when validation fails."""
    pass


class NotFoundError(BusinessLogicError):
    """Raised when an entity is not found."""
    pass


class DuplicateError(BusinessLogicError):
    """Raised when trying to create a duplicate entity."""
    pass


class PermissionError(BusinessLogicError):
    """Raised when user doesn't have permission."""
    pass


class InvalidOperationError(BusinessLogicError):
    """Raised when an operation is invalid."""
    pass
