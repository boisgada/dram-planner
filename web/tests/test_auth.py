"""
Tests for authentication API endpoints.
"""

import pytest
from app.models import User, db


class TestRegistration:
    """Test user registration."""
    
    def test_register_user_success(self, client, app):
        """Test successful user registration."""
        with app.app_context():
            response = client.post('/api/auth/register', json={
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password': 'password123'
            })
            
            assert response.status_code == 201
            data = response.get_json()
            assert data['username'] == 'newuser'
            assert data['email'] == 'newuser@example.com'
            
            # Verify user was created in database
            user = User.query.filter_by(username='newuser').first()
            assert user is not None
            assert user.check_password('password123')
    
    def test_register_missing_fields(self, client):
        """Test registration with missing fields."""
        response = client.post('/api/auth/register', json={
            'username': 'newuser'
        })
        assert response.status_code == 400
    
    def test_register_duplicate_username(self, client, app, user):
        """Test registration with duplicate username."""
        with app.app_context():
            response = client.post('/api/auth/register', json={
                'username': user.username,
                'email': 'different@example.com',
                'password': 'password123'
            })
            assert response.status_code == 400
            data = response.get_json()
            assert 'error' in data
    
    def test_register_duplicate_email(self, client, app, user):
        """Test registration with duplicate email."""
        with app.app_context():
            response = client.post('/api/auth/register', json={
                'username': 'differentuser',
                'email': user.email,
                'password': 'password123'
            })
            assert response.status_code == 400


class TestLogin:
    """Test user login."""
    
    def test_login_success(self, client, app, user):
        """Test successful login."""
        with app.app_context():
            response = client.post('/api/auth/login', json={
                'username': user.username,
                'password': 'testpass123'
            })
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['username'] == user.username
            assert data['email'] == user.email
    
    def test_login_invalid_username(self, client):
        """Test login with invalid username."""
        response = client.post('/api/auth/login', json={
            'username': 'nonexistent',
            'password': 'password123'
        })
        assert response.status_code == 401
    
    def test_login_invalid_password(self, client, app, user):
        """Test login with invalid password."""
        with app.app_context():
            response = client.post('/api/auth/login', json={
                'username': user.username,
                'password': 'wrongpassword'
            })
            assert response.status_code == 401
    
    def test_login_missing_fields(self, client):
        """Test login with missing fields."""
        response = client.post('/api/auth/login', json={
            'username': 'testuser'
        })
        assert response.status_code == 400


class TestLogout:
    """Test user logout."""
    
    def test_logout_success(self, client, app, logged_in_user):
        """Test successful logout."""
        with app.app_context():
            response = client.post('/api/auth/logout')
            assert response.status_code == 200
    
    def test_logout_not_logged_in(self, client):
        """Test logout when not logged in."""
        response = client.post('/api/auth/logout')
        assert response.status_code == 401 or response.status_code == 302

