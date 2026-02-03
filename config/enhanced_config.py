#!/usr/bin/python3
"""
Enhanced configuration module for HBNB
"""
import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
from datetime import timedelta

# Load environment variables
load_dotenv()


class EnhancedConfig:
    """
    Enhanced configuration with environment-specific settings
    """
    
    # Environment
    ENV = os.getenv('HBNB_ENV', 'development')
    DEBUG = ENV == 'development'
    TESTING = ENV == 'testing'
    
    # Security
    SECRET_KEY = os.getenv('HBNB_SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('HBNB_JWT_SECRET', 'jwt-secret-change-me')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('HBNB_DATABASE_URI',
        'mysql+mysqldb://hbnb_dev:hbnb_dev_pwd@localhost/hbnb_dev_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = int(os.getenv('HBNB_DB_POOL_SIZE', 20))
    SQLALCHEMY_MAX_OVERFLOW = int(os.getenv('HBNB_DB_MAX_OVERFLOW', 30))
    SQLALCHEMY_POOL_RECYCLE = int(os.getenv('HBNB_DB_POOL_RECYCLE', 3600))
    
    # Redis Cache
    REDIS_HOST = os.getenv('HBNB_REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('HBNB_REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('HBNB_REDIS_DB', 0))
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('HBNB_CACHE_TIMEOUT', 300))
    
    # File Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.getenv('HBNB_UPLOAD_FOLDER', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    
    # API Settings
    API_PREFIX = '/api/v1'
    API_TITLE = 'HBNB Enhanced API'
    API_VERSION = '1.1.0'
    SWAGGER_UI_DOC_EXPANSION = 'list'
    SWAGGER_UI_JSONEDITOR = True
    
    # Pagination
    DEFAULT_PAGE_SIZE = int(os.getenv('HBNB_DEFAULT_PAGE_SIZE', 10))
    MAX_PAGE_SIZE = int(os.getenv('HBNB_MAX_PAGE_SIZE', 100))
    
    # Rate Limiting
    RATELIMIT_ENABLED = os.getenv('HBNB_RATELIMIT_ENABLED', 'true').lower() == 'true'
    RATELIMIT_DEFAULT = os.getenv('HBNB_RATELIMIT_DEFAULT', '100 per minute')
    RATELIMIT_STORAGE_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    
    # Email
    MAIL_SERVER = os.getenv('HBNB_MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('HBNB_MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('HBNB_MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.getenv('HBNB_MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('HBNB_MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('HBNB_MAIL_SENDER', 'noreply@hbnb.com')
    
    # Monitoring
    ENABLE_METRICS = os.getenv('HBNB_ENABLE_METRICS', 'false').lower() == 'true'
    METRICS_PORT = int(os.getenv('HBNB_METRICS_PORT', 9090))
    
    # Logging Configuration
    @staticmethod
    def setup_logging(app):
        """Configure application logging"""
        
        # Create logs directory if it doesn't exist
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Set log level based on environment
        log_level = logging.DEBUG if app.config['DEBUG'] else logging.INFO
        
        # Configure root logger
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # File handler for errors
        error_handler = RotatingFileHandler(
            f'{log_dir}/error.log',
            maxBytes=10000000,  # 10MB
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s'
        ))
        
        # File handler for all logs
        all_handler = RotatingFileHandler(
            f'{log_dir}/app.log',
            maxBytes=10000000,  # 10MB
            backupCount=5
        )
        all_handler.setLevel(logging.INFO)
        all_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        
        # Console handler for development
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(logging.Formatter(
            '%(levelname)s - %(message)s'
        ))
        
        # Apply handlers
        app.logger.addHandler(error_handler)
        app.logger.addHandler(all_handler)
        
        if app.config['DEBUG']:
            app.logger.addHandler(console_handler)
        
        app.logger.setLevel(log_level)
    
    # Performance Settings
    @staticmethod
    def get_performance_settings():
        """Get performance-related settings"""
        return {
            'database': {
                'query_timeout': int(os.getenv('HBNB_DB_QUERY_TIMEOUT', 30)),
                'connection_timeout': int(os.getenv('HBNB_DB_CONN_TIMEOUT', 10)),
                'enable_query_logging': os.getenv('HBNB_DB_QUERY_LOGGING', 'false').lower() == 'true'
            },
            'cache': {
                'enabled': os.getenv('HBNB_CACHE_ENABLED', 'true').lower() == 'true',
                'strategy': os.getenv('HBNB_CACHE_STRATEGY', 'lru'),
                'compression': os.getenv('HBNB_CACHE_COMPRESSION', 'false').lower() == 'true'
            },
            'api': {
                'compression': os.getenv('HBNB_API_COMPRESSION', 'true').lower() == 'true',
                'cors_enabled': os.getenv('HBNB_CORS_ENABLED', 'true').lower() == 'true',
                'cors_origins': os.getenv('HBNB_CORS_ORIGINS', '*').split(',')
            }
        }
    
    # Feature Flags
    @staticmethod
    def get_feature_flags():
        """Get feature flag configuration"""
        return {
            'enable_recommendations': os.getenv('HBNB_FEATURE_RECOMMENDATIONS', 'false').lower() == 'true',
            'enable_analytics': os.getenv('HBNB_FEATURE_ANALYTICS', 'false').lower() == 'true',
            'enable_notifications': os.getenv('HBNB_FEATURE_NOTIFICATIONS', 'true').lower() == 'true',
            'enable_social_login': os.getenv('HBNB_FEATURE_SOCIAL_LOGIN', 'false').lower() == 'true',
            'enable_booking_validation': os.getenv('HBNB_FEATURE_BOOKING_VALIDATION', 'true').lower() == 'true'
        }


class DevelopmentConfig(EnhancedConfig):
    """Development environment configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    CACHE_DEFAULT_TIMEOUT = 60


class TestingConfig(EnhancedConfig):
    """Testing environment configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    CACHE_DEFAULT_TIMEOUT = 0  # Disable cache for testing


class ProductionConfig(EnhancedConfig):
    """Production environment configuration"""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    CACHE_DEFAULT_TIMEOUT = 600  # 10 minutes
    
    # Security hardening
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
