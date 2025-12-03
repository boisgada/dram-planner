"""
Advanced Tasting Customization API endpoints
Part of ENH-011: Advanced Tasting Customization Options
"""

from flask import request, jsonify
from flask_login import login_required, current_user
from app.api import bp
from app.models import UserConfig, db
import json


@bp.route('/config/tasting', methods=['GET'])
@login_required
def get_tasting_config():
    """Get user's advanced tasting configuration."""
    
    config = current_user.config
    if not config:
        # Create default config
        config = UserConfig(user_id=current_user.id)
        db.session.add(config)
        db.session.commit()
    
    return jsonify({
        'bottles_per_session': config.bottles_per_session or 1,
        'rating_scale': config.rating_scale or '0-10',
        'tasting_note_template': config.tasting_note_template,
        'blind_tasting_mode': config.blind_tasting_mode or False,
        'sort_preference': config.sort_preference,
        'exclude_recent_categories_days': config.exclude_recent_categories_days or 0,
        'notification_enabled': config.notification_enabled or False,
        'notification_timing_hours': config.notification_timing_hours or 24
    })


@bp.route('/config/tasting', methods=['PUT'])
@login_required
def update_tasting_config():
    """Update user's advanced tasting configuration."""
    
    config = current_user.config
    if not config:
        config = UserConfig(user_id=current_user.id)
        db.session.add(config)
    
    data = request.get_json() or {}
    
    if 'bottles_per_session' in data:
        bottles = int(data['bottles_per_session'])
        if bottles < 1:
            return jsonify({'error': 'Bottles per session must be at least 1'}), 400
        config.bottles_per_session = bottles
    
    if 'rating_scale' in data:
        valid_scales = ['0-10', '1-5', 'A-F']
        if data['rating_scale'] not in valid_scales:
            return jsonify({'error': f'Rating scale must be one of: {", ".join(valid_scales)}'}), 400
        config.rating_scale = data['rating_scale']
    
    if 'tasting_note_template' in data:
        valid_templates = ['whiskey', 'wine', 'beer', 'cocktail', 'custom', None]
        if data['tasting_note_template'] not in valid_templates:
            return jsonify({'error': 'Invalid tasting note template'}), 400
        config.tasting_note_template = data['tasting_note_template']
    
    if 'blind_tasting_mode' in data:
        config.blind_tasting_mode = bool(data['blind_tasting_mode'])
    
    if 'sort_preference' in data:
        valid_sorts = ['category', 'abv', 'age', 'region', 'price', 'name', None]
        if data['sort_preference'] not in valid_sorts:
            return jsonify({'error': 'Invalid sort preference'}), 400
        config.sort_preference = data['sort_preference']
    
    if 'exclude_recent_categories_days' in data:
        days = int(data['exclude_recent_categories_days'])
        if days < 0:
            return jsonify({'error': 'Days must be non-negative'}), 400
        config.exclude_recent_categories_days = days
    
    if 'notification_enabled' in data:
        config.notification_enabled = bool(data['notification_enabled'])
    
    if 'notification_timing_hours' in data:
        hours = int(data['notification_timing_hours'])
        if hours < 0:
            return jsonify({'error': 'Hours must be non-negative'}), 400
        config.notification_timing_hours = hours
    
    db.session.commit()
    
    return jsonify({
        'message': 'Tasting configuration updated',
        'config': {
            'bottles_per_session': config.bottles_per_session,
            'rating_scale': config.rating_scale,
            'tasting_note_template': config.tasting_note_template,
            'blind_tasting_mode': config.blind_tasting_mode,
            'sort_preference': config.sort_preference,
            'exclude_recent_categories_days': config.exclude_recent_categories_days,
            'notification_enabled': config.notification_enabled,
            'notification_timing_hours': config.notification_timing_hours
        }
    })


@bp.route('/config/tasting/templates', methods=['GET'])
@login_required
def get_tasting_templates():
    """Get available tasting note templates."""
    
    templates = {
        'whiskey': {
            'name': 'Whiskey/Whisky',
            'fields': ['nose', 'palate', 'finish', 'overall', 'notes']
        },
        'wine': {
            'name': 'Wine',
            'fields': ['appearance', 'nose', 'palate', 'finish', 'overall']
        },
        'beer': {
            'name': 'Beer',
            'fields': ['appearance', 'aroma', 'taste', 'mouthfeel', 'overall']
        },
        'cocktail': {
            'name': 'Cocktail',
            'fields': ['appearance', 'aroma', 'taste', 'balance', 'overall']
        },
        'custom': {
            'name': 'Custom',
            'fields': []
        }
    }
    
    return jsonify({'templates': templates})


@bp.route('/config/tasting/rating-scales', methods=['GET'])
@login_required
def get_rating_scales():
    """Get available rating scales."""
    
    scales = {
        '0-10': {
            'name': '0-10 Scale',
            'min': 0,
            'max': 10,
            'description': 'Decimal scale from 0 to 10'
        },
        '1-5': {
            'name': '1-5 Stars',
            'min': 1,
            'max': 5,
            'description': 'Integer star rating from 1 to 5'
        },
        'A-F': {
            'name': 'Letter Grade',
            'min': 'F',
            'max': 'A',
            'description': 'Letter grade from F to A'
        }
    }
    
    return jsonify({'scales': scales})

