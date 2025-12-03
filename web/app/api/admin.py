"""
Admin API endpoints
"""

from flask import request, jsonify
from flask_login import login_required, current_user
from app.api import bp
from app.models import User, db
from functools import wraps


def admin_required_api(f):
    """Decorator to require admin role for API endpoints."""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/admin/users', methods=['GET'])
@admin_required_api
def list_users():
    """List all users (admin only)."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '', type=str)
    
    query = User.query
    
    if search:
        query = query.filter(
            db.or_(
                User.username.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%')
            )
        )
    
    pagination = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    users = [{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin,
        'created_at': user.created_at.isoformat(),
        'last_login': user.last_login.isoformat() if user.last_login else None
    } for user in pagination.items]
    
    return jsonify({
        'users': users,
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    })


@bp.route('/admin/users/<int:user_id>', methods=['GET'])
@admin_required_api
def get_user(user_id):
    """Get user details (admin only)."""
    user = User.query.get_or_404(user_id)
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin,
        'created_at': user.created_at.isoformat(),
        'last_login': user.last_login.isoformat() if user.last_login else None,
        'bottle_count': user.bottles.count(),
        'schedule_count': user.schedules.count()
    })


@bp.route('/admin/users/<int:user_id>', methods=['PUT'])
@admin_required_api
def update_user(user_id):
    """Update user (admin only)."""
    user = User.query.get_or_404(user_id)
    data = request.get_json() or {}
    
    # Prevent modifying own admin status if last admin
    if current_user.id == user_id and 'is_admin' in data:
        admin_count = User.query.filter_by(is_admin=True).count()
        if admin_count <= 1 and not data.get('is_admin', False):
            return jsonify({'error': 'Cannot remove admin status: you are the last admin'}), 400
    
    if 'username' in data:
        # Check if username already exists
        existing = User.query.filter_by(username=data['username']).first()
        if existing and existing.id != user_id:
            return jsonify({'error': 'Username already exists'}), 400
        user.username = data['username']
    
    if 'email' in data:
        # Check if email already exists
        existing = User.query.filter_by(email=data['email']).first()
        if existing and existing.id != user_id:
            return jsonify({'error': 'Email already exists'}), 400
        user.email = data['email']
    
    if 'is_admin' in data:
        user.is_admin = bool(data['is_admin'])
    
    db.session.commit()
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin
    })


@bp.route('/admin/users/<int:user_id>/promote', methods=['POST'])
@admin_required_api
def promote_user(user_id):
    """Promote user to admin (admin only)."""
    user = User.query.get_or_404(user_id)
    
    user.is_admin = True
    db.session.commit()
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'is_admin': user.is_admin,
        'message': f'{user.username} has been promoted to admin'
    })


@bp.route('/admin/users/<int:user_id>/demote', methods=['POST'])
@admin_required_api
def demote_user(user_id):
    """Remove admin status from user (admin only)."""
    user = User.query.get_or_404(user_id)
    
    # Prevent self-demotion if last admin
    if current_user.id == user_id:
        admin_count = User.query.filter_by(is_admin=True).count()
        if admin_count <= 1:
            return jsonify({'error': 'Cannot remove admin status: you are the last admin'}), 400
    
    user.is_admin = False
    db.session.commit()
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'is_admin': user.is_admin,
        'message': f'{user.username} admin status has been removed'
    })


@bp.route('/admin/users/<int:user_id>', methods=['DELETE'])
@admin_required_api
def delete_user(user_id):
    """Delete user (admin only)."""
    user = User.query.get_or_404(user_id)
    
    # Prevent self-deletion
    if current_user.id == user_id:
        return jsonify({'error': 'Cannot delete your own account'}), 400
    
    username = user.username
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': f'User {username} has been deleted'})


@bp.route('/admin/stats', methods=['GET'])
@admin_required_api
def admin_stats():
    """Get admin statistics."""
    total_users = User.query.count()
    admin_users = User.query.filter_by(is_admin=True).count()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return jsonify({
        'total_users': total_users,
        'admin_users': admin_users,
        'regular_users': total_users - admin_users,
        'recent_users': [{
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'created_at': u.created_at.isoformat()
        } for u in recent_users]
    })

