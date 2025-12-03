"""
Configuration for Dram Planner Web Application
"""

import os
from pathlib import Path

basedir = Path(__file__).parent.parent


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{basedir / "dram_planner.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Pagination
    BOTTLES_PER_PAGE = 20
    SCHEDULE_ITEMS_PER_PAGE = 50
    
    # File uploads
    UPLOAD_FOLDER = basedir / 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Barcode scanning
    BARCODE_SCANNING_ENABLED = True
    
    # Import/Export
    EXPORT_FOLDER = basedir / 'exports'
    
    # Security settings
    FORCE_HTTPS = os.environ.get('FORCE_HTTPS', 'False').lower() == 'true'
    RATE_LIMIT_ENABLED = True


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    # Use environment variables for sensitive data
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

