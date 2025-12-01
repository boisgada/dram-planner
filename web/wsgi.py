#!/usr/bin/env python3
"""
WSGI entry point for Dram Planner Web Application
Used by Gunicorn in production
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from config import config

# Get environment or default to production
env = os.getenv('FLASK_ENV', 'production')
config_class = config.get(env, config['default'])

application = create_app(config_class)

if __name__ == '__main__':
    application.run()

