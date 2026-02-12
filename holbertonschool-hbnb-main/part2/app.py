#!/usr/bin/env python3
"""Main application file"""
from flask import Flask
from flask_cors import CORS
from api import api_bp

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    CORS(app, origins=["http://127.0.0.1:5500", "http://localhost:5500"], supports_credentials=True)
    # Register API blueprint
    app.register_blueprint(api_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("Starting HBnB API on http://localhost:5000")
    print("API docs: http://localhost:5000/api/v1/docs")
    app.run(debug=True, host='0.0.0.0', port=5000)
