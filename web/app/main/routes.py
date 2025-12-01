"""
Main routes
"""

from flask import render_template, redirect, url_for
from app.main import bp
from flask_login import login_required, current_user


@bp.route('/')
def index():
    """Home page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')


@bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard."""
    return render_template('dashboard.html')


@bp.route('/collection')
@login_required
def collection():
    """Collection management page."""
    return render_template('collection.html')


@bp.route('/schedule')
@login_required
def schedule():
    """Schedule viewing page."""
    return render_template('schedule.html')


@bp.route('/settings')
@login_required
def settings():
    """Settings/preferences page."""
    return render_template('settings.html')


@bp.route('/catalog')
@login_required
def catalog():
    """Beverage catalog browsing page."""
    return render_template('catalog.html')


@bp.route('/groups')
@login_required
def groups():
    """User groups page."""
    return render_template('groups.html')

