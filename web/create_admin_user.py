#!/usr/bin/env python3
"""
Helper script to create the first admin user.
Usage: python create_admin_user.py <username> <email> <password>
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User
from config import Config


def create_admin_user(username, email, password):
    """Create an admin user."""
    app = create_app(Config)
    
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            if existing_user.is_admin:
                print(f"User '{username}' already exists and is already an admin.")
                return False
            else:
                # Promote existing user to admin
                existing_user.is_admin = True
                db.session.commit()
                print(f"User '{username}' already exists. Promoted to admin.")
                return True
        
        # Check if email is already taken
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            print(f"Email '{email}' is already registered to another user.")
            return False
        
        # Create new admin user
        admin_user = User(
            username=username,
            email=email,
            is_admin=True
        )
        admin_user.set_password(password)
        
        db.session.add(admin_user)
        db.session.commit()
        
        print(f"Admin user '{username}' created successfully!")
        return True


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python create_admin_user.py <username> <email> <password>")
        sys.exit(1)
    
    username = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    
    if create_admin_user(username, email, password):
        sys.exit(0)
    else:
        sys.exit(1)

