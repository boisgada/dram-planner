"""
Tests for database models.
"""

import pytest
from datetime import date, datetime
from app.models import User, Bottle, Schedule, ScheduleItem, UserConfig, db


class TestUser:
    """Test User model."""
    
    def test_create_user(self, app, db_session):
        """Test creating a user."""
        user = User(
            username='testuser',
            email='test@example.com'
        )
        user.set_password('password123')
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.is_admin is False
        assert user.check_password('password123')
        assert not user.check_password('wrongpassword')
    
    def test_user_password_hashing(self, app, db_session):
        """Test password hashing."""
        user = User(username='test', email='test@test.com')
        user.set_password('password123')
        
        assert user.password_hash != 'password123'
        assert user.password_hash is not None
        assert len(user.password_hash) > 0
    
    def test_user_is_admin(self, app, db_session):
        """Test admin user creation."""
        admin = User(
            username='admin',
            email='admin@example.com',
            is_admin=True
        )
        admin.set_password('adminpass')
        db_session.add(admin)
        db_session.commit()
        
        assert admin.is_admin is True


class TestBottle:
    """Test Bottle model."""
    
    def test_create_bottle(self, app, db_session, user):
        """Test creating a bottle."""
        bottle = Bottle(
            user_id=user.id,
            name='Test Whisky',
            category='scotch',
            abv=43.0,
            price_paid=75.00
        )
        db_session.add(bottle)
        db_session.commit()
        
        assert bottle.id is not None
        assert bottle.name == 'Test Whisky'
        assert bottle.category == 'scotch'
        assert bottle.user_id == user.id
        assert bottle.tasted is False
    
    def test_bottle_to_dict(self, app, db_session, user):
        """Test bottle serialization."""
        bottle = Bottle(
            user_id=user.id,
            name='Test Bottle',
            category='bourbon',
            abv=40.0
        )
        db_session.add(bottle)
        db_session.commit()
        
        data = bottle.to_dict()
        assert data['name'] == 'Test Bottle'
        assert data['category'] == 'bourbon'
        assert data['abv'] == 40.0
        assert 'id' in data
        assert 'created_at' in data


class TestSchedule:
    """Test Schedule model."""
    
    def test_create_schedule(self, app, db_session, user):
        """Test creating a schedule."""
        schedule = Schedule(
            user_id=user.id,
            name='My Tasting Schedule',
            start_date=date.today(),
            weeks=52
        )
        db_session.add(schedule)
        db_session.commit()
        
        assert schedule.id is not None
        assert schedule.name == 'My Tasting Schedule'
        assert schedule.user_id == user.id
        assert schedule.weeks == 52
    
    def test_schedule_to_dict(self, app, db_session, user):
        """Test schedule serialization."""
        schedule = Schedule(
            user_id=user.id,
            name='Test Schedule',
            start_date=date.today(),
            weeks=26
        )
        db_session.add(schedule)
        db_session.commit()
        
        data = schedule.to_dict()
        assert data['name'] == 'Test Schedule'
        assert data['weeks'] == 26
        assert 'id' in data
        assert 'items' in data


class TestUserConfig:
    """Test UserConfig model."""
    
    def test_create_user_config(self, app, db_session, user):
        """Test creating user config."""
        config = UserConfig(
            user_id=user.id,
            tasting_frequency='weekly',
            custom_interval_days=7
        )
        db_session.add(config)
        db_session.commit()
        
        assert config.user_id == user.id
        assert config.tasting_frequency == 'weekly'
        assert config.seasonal_adjustments is False

