from flask import Flask
from flask_restx import Api
from config import config
import os

def create_app(config_name='default'):
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='A REST API for HBnB clone',
        doc='/api/v1/docs/'
    )
    
    # Register blueprints/namespaces
    from presentation.api.v1.routes import api as api_v1
    api.add_namespace(api_v1, path='/api/v1')
    
    return app


# For testing configuration
class TestConfig:
    """Testing configuration."""
    TESTING = True
    SECRET_KEY = 'test-secret-key'
    DEBUG = True
    JSON_SORT_KEYS = False

# Update config dictionary
config['testing'] = TestConfig
