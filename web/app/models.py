"""
Database Models for Dram Planner Web Application
"""

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(UserMixin, db.Model):
    """User model for authentication."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    bottles = db.relationship('Bottle', backref='owner', lazy='dynamic', cascade='all, delete-orphan')
    schedules = db.relationship('Schedule', backref='owner', lazy='dynamic', cascade='all, delete-orphan')
    config = db.relationship('UserConfig', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Set password hash."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Bottle(db.Model):
    """Bottle model."""
    __tablename__ = 'bottles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False, index=True)
    abv = db.Column(db.Float, default=0.0)
    price_paid = db.Column(db.Float, default=0.0)
    purchase_date = db.Column(db.Date)
    opened_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    barcode = db.Column(db.String(50), index=True)
    photo_path = db.Column(db.String(255))
    
    # Tasting information
    tasted = db.Column(db.Boolean, default=False, index=True)
    tasting_date = db.Column(db.Date)
    rating = db.Column(db.Float)
    tasting_notes = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'abv': self.abv,
            'price_paid': self.price_paid,
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None,
            'opened_date': self.opened_date.isoformat() if self.opened_date else None,
            'notes': self.notes,
            'barcode': self.barcode,
            'photo_path': self.photo_path,
            'photo_url': f'/api/bottles/{self.id}/photo' if self.photo_path else None,
            'tasted': self.tasted,
            'tasting_date': self.tasting_date.isoformat() if self.tasting_date else None,
            'rating': self.rating,
            'tasting_notes': self.tasting_notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Bottle {self.name}>'


class Schedule(db.Model):
    """Schedule model."""
    __tablename__ = 'schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    weeks = db.Column(db.Integer, nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    items = db.relationship('ScheduleItem', backref='schedule', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            'id': self.id,
            'name': self.name,
            'start_date': self.start_date.isoformat(),
            'weeks': self.weeks,
            'generated_at': self.generated_at.isoformat(),
            'items': [item.to_dict() for item in self.items]
        }
    
    def __repr__(self):
        return f'<Schedule {self.name}>'


class ScheduleItem(db.Model):
    """Schedule item model."""
    __tablename__ = 'schedule_items'
    
    id = db.Column(db.Integer, primary_key=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.id'), nullable=False, index=True)
    bottle_id = db.Column(db.Integer, db.ForeignKey('bottles.id'), nullable=False, index=True)
    week = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    is_repeat = db.Column(db.Boolean, default=False)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    
    # Relationship
    bottle = db.relationship('Bottle', backref='schedule_items')
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            'id': self.id,
            'schedule_id': self.schedule_id,
            'bottle_id': self.bottle_id,
            'bottle': self.bottle.to_dict() if self.bottle else None,
            'week': self.week,
            'date': self.date.isoformat(),
            'is_repeat': self.is_repeat,
            'completed': self.completed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    def __repr__(self):
        return f'<ScheduleItem week={self.week} date={self.date}>'


class UserConfig(db.Model):
    """User configuration/preferences model."""
    __tablename__ = 'user_configs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    
    # Preferences
    tasting_frequency = db.Column(db.String(20), default='weekly')
    custom_interval_days = db.Column(db.Integer, default=7)
    preferred_days = db.Column(db.String(100))  # JSON array as string
    avoid_dates = db.Column(db.Text)  # JSON array as string
    category_preferences = db.Column(db.Text)  # JSON object as string
    seasonal_adjustments = db.Column(db.Boolean, default=False)
    min_days_between_category = db.Column(db.Integer, default=0)
    default_schedule_weeks = db.Column(db.Integer, default=104)
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary."""
        import json
        return {
            'tasting_frequency': self.tasting_frequency,
            'custom_interval_days': self.custom_interval_days,
            'preferred_days': json.loads(self.preferred_days) if self.preferred_days else [],
            'avoid_dates': json.loads(self.avoid_dates) if self.avoid_dates else [],
            'category_preferences': json.loads(self.category_preferences) if self.category_preferences else {},
            'seasonal_adjustments': self.seasonal_adjustments,
            'min_days_between_category': self.min_days_between_category,
            'default_schedule_weeks': self.default_schedule_weeks
        }
    
    def __repr__(self):
        return f'<UserConfig user_id={self.user_id}>'

