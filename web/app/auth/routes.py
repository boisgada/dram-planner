"""
Authentication routes
"""

from flask import render_template, redirect, url_for, flash, request
from app.auth import bp
from app.models import User
from app import db
from flask_login import login_user, logout_user, login_required, current_user
from app.auth.forms import LoginForm, RegistrationForm


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        flash('Invalid username or password')
    
    return render_template('auth/login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        # Create default config
        from app.models import UserConfig
        config = UserConfig(user_id=user.id)
        db.session.add(config)
        db.session.commit()
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

