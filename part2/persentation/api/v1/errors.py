"""Custom error handlers for API v1."""

from flask import jsonify
from flask_restx import Api

api = Api(
    version='1.0',
    title='HBnB API',
    description='HBnB API v1',
    doc='/api/v1/docs'
)

@api.errorhandler
def default_error_handler(e):
    """Default error handler."""
    message = 'An unhandled exception occurred.'
    return {'message': message}, 500

@api.errorhandler(404)
def not_found_error_handler(e):
    """404 error handler."""
    return {'message': 'Resource not found'}, 404

@api.errorhandler(400)
def bad_request_error_handler(e):
    """400 error handler."""
    return {'message': 'Bad request'}, 400
