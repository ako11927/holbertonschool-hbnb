"App initialization for HBnB."
from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Create API
    api = Api(app, version="1.0", title="HBnB API", description="HBnB Application API", doc="/api/v1/")

    # Register namespaces
    from .api.v1.users import api as users_ns
    api.add_namespace(users_ns, path="/api/v1/users")

    return app

