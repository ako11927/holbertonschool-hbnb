"""Custom error handlers for API v1."""

from flask import jsonify

# Error handlers will be registered by the main API
# This file just contains the handler functions

def default_error_handler(e):
    """Default error handler."""
    message = 'An unhandled exception occurred.'
    return {'message': message}, 500

def not_found_error_handler(e):
    """404 error handler."""
    return {'message': 'Resource not found'}, 404

def bad_request_error_handler(e):
    """400 error handler."""
    return {'message': 'Bad request'}, 400
