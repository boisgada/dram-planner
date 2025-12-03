"""
Tests for admin API endpoints.
"""

import pytest
from app.models import User, db


class TestAdminAPI:
    """Test admin API endpoints."""
    
    def test_list_users_requires_admin(self, client, app, logged_in_user):
        """Test listing users requires admin."""
        with app.app_context():
            response = client.get('/api/admin/users')
            assert response.status_code == 403
    
    def test_list_users_as_admin(self, client, app, logged_in_admin):
        """Test listing users as admin."""
        with app.app_context():
            # Create additional users
            user2 = User(username='user2', email='user2@example.com')
            user2.set_password('pass123')
            db.session.add(user2)
            db.session.commit()
            
            response = client.get('/api/admin/users')
            assert response.status_code == 200
            data = response.get_json()
            assert 'users' in data
            assert len(data['users']) >= 2
    
    def test_get_user_details(self, client, app, logged_in_admin, user):
        """Test getting user details as admin."""
        with app.app_context():
            response = client.get(f'/api/admin/users/{user.id}')
            assert response.status_code == 200
            data = response.get_json()
            assert data['id'] == user.id
            assert data['username'] == user.username
    
    def test_promote_user_to_admin(self, client, app, logged_in_admin, user):
        """Test promoting user to admin."""
        with app.app_context():
            assert user.is_admin is False
            
            response = client.post(f'/api/admin/users/{user.id}/promote')
            assert response.status_code == 200
            
            # Verify promotion
            user = User.query.get(user.id)
            assert user.is_admin is True
    
    def test_demote_user_from_admin(self, client, app, logged_in_admin):
        """Test demoting admin user."""
        with app.app_context():
            # Create another admin
            admin2 = User(username='admin2', email='admin2@example.com', is_admin=True)
            admin2.set_password('pass123')
            db.session.add(admin2)
            db.session.commit()
            
            response = client.post(f'/api/admin/users/{admin2.id}/demote')
            assert response.status_code == 200
            
            # Verify demotion
            admin2 = User.query.get(admin2.id)
            assert admin2.is_admin is False
    
    def test_update_user(self, client, app, logged_in_admin, user):
        """Test updating user as admin."""
        with app.app_context():
            response = client.put(f'/api/admin/users/{user.id}', json={
                'username': 'updated_username',
                'email': 'updated@example.com'
            })
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['username'] == 'updated_username'
            
            # Verify update
            user = User.query.get(user.id)
            assert user.username == 'updated_username'
    
    def test_delete_user(self, client, app, logged_in_admin):
        """Test deleting user as admin."""
        with app.app_context():
            # Create user to delete
            user_to_delete = User(username='todelete', email='delete@example.com')
            user_to_delete.set_password('pass123')
            db.session.add(user_to_delete)
            db.session.commit()
            user_id = user_to_delete.id
            
            response = client.delete(f'/api/admin/users/{user_id}')
            assert response.status_code == 200
            
            # Verify deletion
            user = User.query.get(user_id)
            assert user is None
    
    def test_admin_stats(self, client, app, logged_in_admin):
        """Test getting admin statistics."""
        with app.app_context():
            response = client.get('/api/admin/stats')
            assert response.status_code == 200
            data = response.get_json()
            assert 'total_users' in data
            assert 'admin_users' in data
            assert data['total_users'] >= 1

