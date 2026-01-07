from flask import Flask
from config import config
import os

def create_app(config_name='default'):
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Import and initialize the API from routes
    from presentation.api.v1.routes import api
    api.init_app(app)
    
    return app
