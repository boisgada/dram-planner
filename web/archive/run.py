#!/usr/bin/env python3
"""
Run script for Dram Planner Web Application
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from config import config

# Get environment or default to development
env = os.getenv('FLASK_ENV', 'development')
config_class = config.get(env, config['default'])

app = create_app(config_class)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)

