from flask import Flask
from flask_restx import Api

def create_app():
    app = Flask(__name__)
    
    # Import and register the API blueprint
    try:
        from .api.v1.routes import blueprint as api_v1_blueprint
        app.register_blueprint(api_v1_blueprint)
    except ImportError:
        # Fallback if routes aren't ready
        api = Api(app, version='1.0', title='HBnB API', 
                 description='HBnB Application API', doc='/api/v1/')
    
    return app
