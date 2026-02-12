#!/usr/bin/env python3
"""Main application file. Flask + Flask-RESTx + JWT + Bcrypt."""
import os
from flask import Flask
from flask_cors import CORS

from api import api_bp
from config import config
from extensions import bcrypt, jwt   # <-- استيراد من extensions


def create_app(config_name=None):
    """Create and configure the Flask application."""
    config_name = config_name or os.environ.get("FLASK_ENV", "development")
    cfg = config.get(config_name, config["default"])

    app = Flask(__name__)
    app.config.from_object(cfg)

    # إعدادات JWT - ضرورية
    app.config['JWT_SECRET_KEY'] = 'super-secret-key-change-it'
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600

    # Initialize extensions
    jwt.init_app(app)
    bcrypt.init_app(app)
    print("✅ bcrypt initialized")  # تأكد من ظهورها في التيرمنال

    # CORS
    CORS(app, origins=["http://127.0.0.1:5500", "http://localhost:5500"], supports_credentials=True, allow_headers=["Content-Type", "Authorization"])

    # Register blueprint
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    

    # Ensure admin user exists
    with app.app_context():
        from services import facade
        facade.ensure_admin(bcrypt)

    return app


if __name__ == "__main__":
    app = create_app()
    print("Starting HBnB API on http://localhost:5000")
    print("API docs: http://localhost:5000/api/v1/docs")
    app.run(debug=True, host="0.0.0.0", port=5000)