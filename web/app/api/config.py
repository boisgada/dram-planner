"""
Configuration API endpoints
"""

from flask import request, jsonify
from app.api import bp
from app.models import UserConfig
from app import db
from flask_login import login_required, current_user
import json


@bp.route('/config', methods=['GET'])
@login_required
def get_config():
    """Get user configuration."""
    if not current_user.config:
        # Create default config
        config = UserConfig(user_id=current_user.id)
        db.session.add(config)
        db.session.commit()
        current_user.config = config
    
    return jsonify(current_user.config.to_dict())


@bp.route('/config', methods=['PUT'])
@login_required
def update_config():
    """Update user configuration."""
    if not current_user.config:
        config = UserConfig(user_id=current_user.id)
        db.session.add(config)
    else:
        config = current_user.config
    
    data = request.get_json() or {}
    
    if 'tasting_frequency' in data:
        config.tasting_frequency = data['tasting_frequency']
    if 'custom_interval_days' in data:
        config.custom_interval_days = data['custom_interval_days']
    if 'preferred_days' in data:
        config.preferred_days = json.dumps(data['preferred_days'])
    if 'avoid_dates' in data:
        config.avoid_dates = json.dumps(data['avoid_dates'])
    if 'category_preferences' in data:
        config.category_preferences = json.dumps(data['category_preferences'])
    if 'seasonal_adjustments' in data:
        config.seasonal_adjustments = data['seasonal_adjustments']
    if 'min_days_between_category' in data:
        config.min_days_between_category = data['min_days_between_category']
    if 'default_schedule_weeks' in data:
        config.default_schedule_weeks = data['default_schedule_weeks']
    
    from datetime import datetime
    config.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(config.to_dict())

