from flask import Flask, jsonify
from config import config

def create_app(config_name='default'):
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Import and register the API blueprint
    from presentation.api.v1.routes import blueprint as api_v1_blueprint
    app.register_blueprint(api_v1_blueprint)
    
    # Register error handlers at Flask level
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'message': 'Resource not found'}), 404
    
    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({'message': 'Bad request'}), 400
    
    @app.errorhandler(Exception)
    def internal_error(error):
        return jsonify({'message': 'An internal error occurred'}), 500
    
    return app
