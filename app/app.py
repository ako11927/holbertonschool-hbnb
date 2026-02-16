#!/usr/bin/env python3
"""Main application file"""
from flask import Flask
from api import api_bp

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Register API blueprint
    app.register_blueprint(api_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("Starting HBnB API on http://localhost:5000")
    print("API docs: http://localhost:5000/api/v1/docs")
    app.run(debug=True, host='0.0.0.0', port=5000)
