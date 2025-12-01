"""
Authentication API endpoints
"""

from flask import request, jsonify
from app.api import bp
from app.models import User
from app import db
from flask_login import login_user, logout_user, login_required, current_user


@bp.route('/auth/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json() or {}
    
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Username, email, and password are required'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(
        username=data['username'],
        email=data['email']
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    # Create default config
    from app.models import UserConfig
    config = UserConfig(user_id=user.id)
    db.session.add(config)
    db.session.commit()
    
    login_user(user)
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email
    }), 201


@bp.route('/auth/login', methods=['POST'])
def login():
    """Login user."""
    data = request.get_json() or {}
    
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    login_user(user, remember=data.get('remember', False))
    
    from datetime import datetime
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email
    })


@bp.route('/auth/logout', methods=['POST'])
@login_required
def logout():
    """Logout user."""
    logout_user()
    return jsonify({'message': 'Logged out successfully'})


@bp.route('/auth/me', methods=['GET'])
@login_required
def get_current_user():
    """Get current user information."""
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email
    })

