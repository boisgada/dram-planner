"""
Admin routes for user management
"""

from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.admin import bp
from app.models import User, db
from functools import wraps


def admin_required(f):
    """Decorator to require admin role."""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Admin access required.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/users')
@admin_required
def users():
    """Admin user management page."""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    per_page = 20
    
    query = User.query
    
    if search:
        query = query.filter(
            db.or_(
                User.username.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%')
            )
        )
    
    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin/users.html', users=users, search=search)


@bp.route('/users/<int:user_id>')
@admin_required
def user_detail(user_id):
    """View user details."""
    user = User.query.get_or_404(user_id)
    return render_template('admin/user_detail.html', user=user)


@bp.route('/users/<int:user_id>/promote', methods=['POST'])
@admin_required
def promote_user(user_id):
    """Promote user to admin."""
    user = User.query.get_or_404(user_id)
    
    # Prevent self-demotion if this is the last admin
    if current_user.id == user_id:
        admin_count = User.query.filter_by(is_admin=True).count()
        if admin_count <= 1:
            flash('Cannot remove admin status: you are the last admin.', 'error')
            return redirect(url_for('admin.user_detail', user_id=user_id))
    
    user.is_admin = True
    db.session.commit()
    flash(f'{user.username} has been promoted to admin.', 'success')
    return redirect(url_for('admin.user_detail', user_id=user_id))


@bp.route('/users/<int:user_id>/demote', methods=['POST'])
@admin_required
def demote_user(user_id):
    """Remove admin status from user."""
    user = User.query.get_or_404(user_id)
    
    # Prevent self-demotion if this is the last admin
    if current_user.id == user_id:
        admin_count = User.query.filter_by(is_admin=True).count()
        if admin_count <= 1:
            flash('Cannot remove admin status: you are the last admin.', 'error')
            return redirect(url_for('admin.user_detail', user_id=user_id))
    
    user.is_admin = False
    db.session.commit()
    flash(f'{user.username} admin status has been removed.', 'success')
    return redirect(url_for('admin.user_detail', user_id=user_id))


@bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    """Delete a user account."""
    user = User.query.get_or_404(user_id)
    
    # Prevent self-deletion
    if current_user.id == user_id:
        flash('Cannot delete your own account.', 'error')
        return redirect(url_for('admin.user_detail', user_id=user_id))
    
    username = user.username
    db.session.delete(user)
    db.session.commit()
    flash(f'User {username} has been deleted.', 'success')
    return redirect(url_for('admin.users'))


@bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard."""
    total_users = User.query.count()
    admin_users = User.query.filter_by(is_admin=True).count()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         admin_users=admin_users,
                         recent_users=recent_users)

