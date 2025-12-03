"""
Tests for advanced tasting customization API endpoints
Part of ENH-011: Advanced Tasting Customization Options
"""

import pytest
from app.models import UserConfig, db


def test_get_tasting_config(client, logged_in_user):
    """Test getting user's tasting configuration."""
    response = client.get('/api/config/tasting')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'bottles_per_session' in data
    assert 'rating_scale' in data
    assert 'tasting_note_template' in data


def test_update_tasting_config(client, logged_in_user, db_session):
    """Test updating tasting configuration."""
    response = client.put('/api/config/tasting', json={
        'bottles_per_session': 3,
        'rating_scale': '1-5',
        'blind_tasting_mode': True
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['config']['bottles_per_session'] == 3
    assert data['config']['rating_scale'] == '1-5'
    assert data['config']['blind_tasting_mode'] is True


def test_update_invalid_rating_scale(client, logged_in_user):
    """Test updating with invalid rating scale."""
    response = client.put('/api/config/tasting', json={
        'rating_scale': 'invalid'
    })
    
    assert response.status_code == 400


def test_update_invalid_bottles_per_session(client, logged_in_user):
    """Test updating with invalid bottles per session."""
    response = client.put('/api/config/tasting', json={
        'bottles_per_session': 0  # Must be at least 1
    })
    
    assert response.status_code == 400


def test_get_tasting_templates(client, logged_in_user):
    """Test getting available tasting note templates."""
    response = client.get('/api/config/tasting/templates')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'templates' in data
    assert 'whiskey' in data['templates']
    assert 'wine' in data['templates']


def test_get_rating_scales(client, logged_in_user):
    """Test getting available rating scales."""
    response = client.get('/api/config/tasting/rating-scales')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'scales' in data
    assert '0-10' in data['scales']
    assert '1-5' in data['scales']
    assert 'A-F' in data['scales']

