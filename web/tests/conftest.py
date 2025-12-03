"""
Pytest configuration and fixtures for web application tests.
"""

import pytest
import sys
import os
from pathlib import Path

# Add web directory to path
web_dir = Path(__file__).parent.parent
sys.path.insert(0, str(web_dir))

from app import create_app, db
from app.models import User, Bottle, Schedule, ScheduleItem, UserConfig
from config import TestingConfig


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app(TestingConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test CLI runner."""
    return app.test_cli_runner()


@pytest.fixture
def auth(client):
    """Authentication helper fixture."""
    class AuthActions:
        def __init__(self, client):
            self._client = client
        
        def register(self, username='testuser', email='test@example.com', password='testpass123'):
            """Register a new user."""
            return self._client.post('/api/auth/register', json={
                'username': username,
                'email': email,
                'password': password
            })
        
        def login(self, username='testuser', password='testpass123'):
            """Login user."""
            return self._client.post('/api/auth/login', json={
                'username': username,
                'password': password
            })
        
        def logout(self):
            """Logout user."""
            return self._client.post('/api/auth/logout')
    
    return AuthActions(client)


@pytest.fixture
def user(app, db_session):
    """Create a test user."""
    user = User(
        username='testuser',
        email='test@example.com',
        is_admin=False
    )
    user.set_password('testpass123')
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def admin_user(app, db_session):
    """Create an admin test user."""
    admin = User(
        username='admin',
        email='admin@example.com',
        is_admin=True
    )
    admin.set_password('adminpass123')
    db_session.add(admin)
    db_session.commit()
    return admin


@pytest.fixture
def db_session(app):
    """Create database session for testing."""
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.rollback()
        db.drop_all()


@pytest.fixture
def logged_in_user(client, auth, user):
    """Create a logged-in user session."""
    auth.login(user.username, 'testpass123')
    return user


@pytest.fixture
def logged_in_admin(client, auth, admin_user):
    """Create a logged-in admin session."""
    auth.login(admin_user.username, 'adminpass123')
    return admin_user


@pytest.fixture
def sample_bottle(app, db_session, user):
    """Create a sample bottle for testing."""
    bottle = Bottle(
        user_id=user.id,
        name='Test Bourbon',
        category='bourbon',
        abv=40.0,
        price_paid=50.00
    )
    db_session.add(bottle)
    db_session.commit()
    return bottle


@pytest.fixture
def sample_schedule(app, db_session, user):
    """Create a sample schedule for testing."""
    from datetime import date
    schedule = Schedule(
        user_id=user.id,
        name='Test Schedule',
        start_date=date.today(),
        weeks=52
    )
    db_session.add(schedule)
    db_session.commit()
    return schedule

