"""
Tests for bottles API endpoints.
"""

import pytest
from app.models import Bottle, db


class TestBottlesAPI:
    """Test bottles API endpoints."""
    
    def test_get_bottles_requires_auth(self, client):
        """Test getting bottles requires authentication."""
        response = client.get('/api/bottles')
        assert response.status_code in [401, 302]
    
    def test_get_bottles_empty(self, client, app, logged_in_user):
        """Test getting empty bottles list."""
        with app.app_context():
            response = client.get('/api/bottles')
            assert response.status_code == 200
            data = response.get_json()
            assert 'bottles' in data
            assert len(data['bottles']) == 0
    
    def test_create_bottle(self, client, app, logged_in_user):
        """Test creating a bottle."""
        with app.app_context():
            response = client.post('/api/bottles', json={
                'name': 'New Bottle',
                'category': 'bourbon',
                'abv': 40.0
            })
            
            assert response.status_code == 201
            data = response.get_json()
            assert data['name'] == 'New Bottle'
            assert data['category'] == 'bourbon'
            assert 'id' in data
            
            # Verify in database
            bottle = Bottle.query.filter_by(name='New Bottle').first()
            assert bottle is not None
            assert bottle.user_id == logged_in_user.id
    
    def test_get_bottle_by_id(self, client, app, logged_in_user, sample_bottle):
        """Test getting a specific bottle."""
        with app.app_context():
            response = client.get(f'/api/bottles/{sample_bottle.id}')
            assert response.status_code == 200
            data = response.get_json()
            assert data['id'] == sample_bottle.id
            assert data['name'] == sample_bottle.name
    
    def test_update_bottle(self, client, app, logged_in_user, sample_bottle):
        """Test updating a bottle."""
        with app.app_context():
            response = client.put(f'/api/bottles/{sample_bottle.id}', json={
                'name': 'Updated Bottle',
                'category': 'scotch',
                'abv': 43.0
            })
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['name'] == 'Updated Bottle'
            
            # Verify update in database
            bottle = Bottle.query.get(sample_bottle.id)
            assert bottle.name == 'Updated Bottle'
    
    def test_delete_bottle(self, client, app, logged_in_user, sample_bottle):
        """Test deleting a bottle."""
        with app.app_context():
            bottle_id = sample_bottle.id
            response = client.delete(f'/api/bottles/{bottle_id}')
            assert response.status_code == 200
            
            # Verify deletion
            bottle = Bottle.query.get(bottle_id)
            assert bottle is None
    
    def test_get_bottles_filtered(self, client, app, logged_in_user):
        """Test getting filtered bottles."""
        with app.app_context():
            # Create bottles with different categories
            bottle1 = Bottle(user_id=logged_in_user.id, name='Bourbon 1', category='bourbon')
            bottle2 = Bottle(user_id=logged_in_user.id, name='Scotch 1', category='scotch')
            db.session.add(bottle1)
            db.session.add(bottle2)
            db.session.commit()
            
            # Filter by category
            response = client.get('/api/bottles?category=bourbon')
            assert response.status_code == 200
            data = response.get_json()
            assert all(b['category'] == 'bourbon' for b in data['bottles'])

