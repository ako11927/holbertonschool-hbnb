#!/usr/bin/env python3
"""Main application file. Flask + Flask-RESTx + JWT + Bcrypt."""
import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

from api import api_bp
from config import config

jwt = JWTManager()
bcrypt = Bcrypt()


def create_app(config_name=None):
    """Create and configure the Flask application."""
    config_name = config_name or os.environ.get("FLASK_ENV", "development")
    cfg = config.get(config_name, config["default"])
    app = Flask(__name__)
    app.config.from_object(cfg)

    jwt.init_app(app)
    bcrypt.init_app(app)
    app.register_blueprint(api_bp)

    with app.app_context():
        from services import facade
        facade.ensure_admin(bcrypt)

    return app


if __name__ == "__main__":
    app = create_app()
    print("Starting HBnB API on http://localhost:5000")
    print("API docs: http://localhost:5000/api/v1/docs")
    app.run(debug=True, host="0.0.0.0", port=5000)
