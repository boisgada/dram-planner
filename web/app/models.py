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
    is_admin = db.Column(db.Boolean, default=False, nullable=False, index=True)
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
    
    # Advanced tasting customization (ENH-011)
    bottles_per_session = db.Column(db.Integer, default=1)
    rating_scale = db.Column(db.String(20), default='0-10')  # '0-10', '1-5', 'A-F'
    tasting_note_template = db.Column(db.String(50))  # 'whiskey', 'wine', 'beer', 'custom'
    blind_tasting_mode = db.Column(db.Boolean, default=False)
    sort_preference = db.Column(db.String(50))  # 'category', 'abv', 'age', 'region', 'price'
    exclude_recent_categories_days = db.Column(db.Integer, default=0)
    notification_enabled = db.Column(db.Boolean, default=False)
    notification_timing_hours = db.Column(db.Integer, default=24)
    
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


class MasterBeverage(db.Model):
    """Master catalog of beverages for quick selection."""
    __tablename__ = 'master_beverages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    brand = db.Column(db.String(255), index=True)
    category = db.Column(db.String(50), nullable=False, index=True)
    subcategory = db.Column(db.String(100))
    abv = db.Column(db.Float)
    region = db.Column(db.String(100))
    country = db.Column(db.String(100))
    description = db.Column(db.Text)
    tasting_notes = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    external_id = db.Column(db.String(100))  # For external API references
    source = db.Column(db.String(50))  # 'internal', 'openfoodfacts', etc.
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'category': self.category,
            'subcategory': self.subcategory,
            'abv': self.abv,
            'region': self.region,
            'country': self.country,
            'description': self.description,
            'tasting_notes': self.tasting_notes,
            'image_url': self.image_url,
            'external_id': self.external_id,
            'source': self.source,
            'verified': self.verified,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        return f'<MasterBeverage {self.name}>'


class UserGroup(db.Model):
    """User groups for shared tasting experiences."""
    __tablename__ = 'user_groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    is_private = db.Column(db.Boolean, default=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    creator = db.relationship('User', backref=db.backref('created_groups', lazy=True))
    members = db.relationship('GroupMembership', back_populates='group', cascade='all, delete-orphan')
    schedules = db.relationship('GroupSchedule', back_populates='group', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_private': self.is_private,
            'created_by': self.creator.username if self.creator else None,
            'member_count': len(self.members),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        return f'<UserGroup {self.name}>'


class GroupMembership(db.Model):
    """Group membership relationships."""
    __tablename__ = 'group_memberships'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('user_groups.id'), nullable=False)
    role = db.Column(db.String(20), default='member')  # 'admin', 'moderator', 'member'
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref=db.backref('group_memberships', lazy=True))
    group = db.relationship('UserGroup', back_populates='members')

    __table_args__ = (db.UniqueConstraint('user_id', 'group_id', name='unique_user_group'),)

    def __repr__(self):
        return f'<GroupMembership user={self.user_id} group={self.group_id}>'


class GroupSchedule(db.Model):
    """Shared schedules for groups."""
    __tablename__ = 'group_schedules'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('user_groups.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    weeks = db.Column(db.Integer, nullable=False, default=52)
    is_active = db.Column(db.Boolean, default=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    group = db.relationship('UserGroup', back_populates='schedules')
    creator = db.relationship('User', backref=db.backref('created_group_schedules', lazy=True))
    items = db.relationship('GroupScheduleItem', back_populates='schedule', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'group_id': self.group_id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date.isoformat(),
            'weeks': self.weeks,
            'is_active': self.is_active,
            'created_by': self.creator.username if self.creator else None,
            'created_at': self.created_at.isoformat(),
            'item_count': len(self.items)
        }

    def __repr__(self):
        return f'<GroupSchedule {self.name}>'


class GroupScheduleItem(db.Model):
    """Individual items in group schedules."""
    __tablename__ = 'group_schedule_items'

    id = db.Column(db.Integer, primary_key=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey('group_schedules.id'), nullable=False)
    week = db.Column(db.Integer, nullable=False)
    tasting_date = db.Column(db.Date, nullable=False)
    bottle_name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50))
    notes = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    completed_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    completed_at = db.Column(db.DateTime)

    # Relationships
    schedule = db.relationship('GroupSchedule', back_populates='items')
    completed_by = db.relationship('User', backref=db.backref('completed_group_items', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'schedule_id': self.schedule_id,
            'week': self.week,
            'tasting_date': self.tasting_date.isoformat(),
            'bottle_name': self.bottle_name,
            'category': self.category,
            'notes': self.notes,
            'completed': self.completed,
            'completed_by': self.completed_by.username if self.completed_by else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

    def __repr__(self):
        return f'<GroupScheduleItem week={self.week} bottle={self.bottle_name}>'


class BeverageReview(db.Model):
    """Community reviews for beverages (ENH-007: Review Visualization & Social Features)."""
    __tablename__ = 'beverage_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    beverage_name = db.Column(db.String(255), nullable=False, index=True)
    beverage_brand = db.Column(db.String(255), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    rating = db.Column(db.Float, nullable=False)  # 0-10 scale
    review_text = db.Column(db.Text)
    is_public = db.Column(db.Boolean, default=True, index=True)
    is_anonymous = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('reviews', lazy='dynamic'))
    
    __table_args__ = (
        db.Index('ix_review_beverage_name_brand', 'beverage_name', 'beverage_brand'),
    )
    
    def to_dict(self, include_user=False):
        """Convert to dictionary for API responses."""
        return {
            'id': self.id,
            'beverage_name': self.beverage_name,
            'beverage_brand': self.beverage_brand,
            'rating': self.rating,
            'review_text': self.review_text,
            'is_public': self.is_public,
            'is_anonymous': self.is_anonymous,
            'username': None if self.is_anonymous else (self.user.username if include_user else None),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<BeverageReview {self.beverage_name} - {self.rating}/10>'
