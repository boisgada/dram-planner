"""
Tests for community reviews API endpoints
Part of ENH-007: Review Visualization & Social Features
"""

import pytest
from app.models import BeverageReview, User, db


def test_create_review(client, logged_in_user):
    """Test creating a new review."""
    response = client.post('/api/reviews', json={
        'beverage_name': 'Test Whisky',
        'beverage_brand': 'Test Brand',
        'rating': 8.5,
        'review_text': 'Great whisky!',
        'is_public': True,
        'is_anonymous': True
    })
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['beverage_name'] == 'Test Whisky'
    assert data['rating'] == 8.5
    assert data['is_public'] is True


def test_create_review_missing_fields(client, logged_in_user):
    """Test creating review with missing required fields."""
    response = client.post('/api/reviews', json={
        'beverage_name': 'Test Whisky'
        # Missing rating
    })
    
    assert response.status_code == 400


def test_get_reviews(client, logged_in_user, db_session):
    """Test getting reviews for a beverage."""
    # Create a test review
    review = BeverageReview(
        beverage_name='Test Whisky',
        beverage_brand='Test Brand',
        user_id=logged_in_user.id,
        rating=8.5,
        review_text='Great!',
        is_public=True
    )
    db_session.add(review)
    db_session.commit()
    
    response = client.get('/api/reviews?beverage_name=Test Whisky')
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['reviews']) >= 1
    assert data['reviews'][0]['beverage_name'] == 'Test Whisky'


def test_get_review_stats(client, logged_in_user, db_session):
    """Test getting review statistics."""
    # Create multiple reviews
    for rating in [7.5, 8.0, 8.5]:
        review = BeverageReview(
            beverage_name='Test Whisky',
            user_id=logged_in_user.id,
            rating=rating,
            is_public=True
        )
        db_session.add(review)
    db_session.commit()
    
    response = client.get('/api/reviews/stats/Test Whisky')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['total_reviews'] == 3
    assert data['average_rating'] is not None
    assert data['average_rating'] > 7.0


def test_get_popular_beverages(client, logged_in_user, db_session):
    """Test getting popular beverages."""
    # Create reviews with different ratings
    for name, rating in [('Whisky A', 9.0), ('Whisky B', 8.5), ('Whisky C', 8.0)]:
        for _ in range(3):  # 3 reviews each
            review = BeverageReview(
                beverage_name=name,
                user_id=logged_in_user.id,
                rating=rating,
                is_public=True
            )
            db_session.add(review)
    db_session.commit()
    
    response = client.get('/api/reviews/popular?limit=10')
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['beverages']) > 0
    # Should be sorted by rating
    assert data['beverages'][0]['average_rating'] >= data['beverages'][-1]['average_rating']


def test_compare_ratings(client, logged_in_user, db_session, sample_bottle):
    """Test comparing user ratings with community averages."""
    # Create community reviews
    review = BeverageReview(
        beverage_name=sample_bottle.name,
        user_id=logged_in_user.id + 1,  # Different user
        rating=7.5,
        is_public=True
    )
    db_session.add(review)
    
    # Set user's bottle rating
    sample_bottle.rating = 8.5
    sample_bottle.tasted = True
    db_session.commit()
    
    response = client.get('/api/reviews/compare')
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['comparisons']) > 0

