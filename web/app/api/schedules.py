"""
Schedules API endpoints
"""

from flask import request, jsonify
from app.api import bp
from app.models import Schedule, ScheduleItem, Bottle
from app import db
from flask_login import login_required, current_user
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path to import CLI modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))
try:
    import schedule_generator
    import config as cli_config
except ImportError:
    schedule_generator = None
    cli_config = None


@bp.route('/schedules', methods=['GET'])
@login_required
def get_schedules():
    """Get all schedules for current user."""
    schedules = Schedule.query.filter_by(user_id=current_user.id).order_by(
        Schedule.generated_at.desc()
    ).all()
    
    return jsonify({
        'schedules': [schedule.to_dict() for schedule in schedules]
    })


@bp.route('/schedules/<int:id>', methods=['GET'])
@login_required
def get_schedule(id):
    """Get a specific schedule."""
    schedule = Schedule.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    return jsonify(schedule.to_dict())


@bp.route('/schedules', methods=['POST'])
@login_required
def create_schedule():
    """Generate a new schedule."""
    data = request.get_json() or {}
    
    # Get user's bottles
    bottles = Bottle.query.filter_by(user_id=current_user.id).all()
    
    if not bottles:
        return jsonify({'error': 'No bottles in collection'}), 400
    
    # Convert to collection format for schedule generator
    collection = {
        'bottles': [{
            'id': b.id,
            'name': b.name,
            'category': b.category,
            'abv': b.abv,
            'tasted': b.tasted
        } for b in bottles]
    }
    
    # Get start date
    start_date_str = data.get('start_date')
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    else:
        start_date = datetime.utcnow().date()
    
    # Get weeks
    weeks = data.get('weeks', 104)
    
    # Get user config if available
    config_data = None
    if current_user.config:
        config_data = current_user.config.to_dict()
        # Convert to format expected by CLI config
        config_data = {
            'user_preferences': config_data
        }
    
    # Generate schedule using CLI module
    if schedule_generator:
        schedule_list = schedule_generator.generate_schedule(
            collection, start_date, weeks, config_data
        )
    else:
        # Fallback: simple schedule generation
        schedule_list = []
        current_date = start_date
        for week in range(weeks):
            if week < len(bottles):
                bottle = bottles[week % len(bottles)]
                schedule_list.append({
                    'week': week + 1,
                    'date': current_date.strftime('%Y-%m-%d'),
                    'bottle_id': bottle.id,
                    'bottle_name': bottle.name,
                    'category': bottle.category,
                    'abv': bottle.abv,
                    'is_repeat': bottle.tasted
                })
                current_date += timedelta(days=7)
    
    # Create schedule in database
    schedule = Schedule(
        user_id=current_user.id,
        name=data.get('name', f'Schedule {datetime.utcnow().strftime("%Y-%m-%d")}'),
        start_date=start_date,
        weeks=weeks
    )
    db.session.add(schedule)
    db.session.flush()
    
    # Create schedule items
    for item_data in schedule_list:
        item = ScheduleItem(
            schedule_id=schedule.id,
            bottle_id=item_data['bottle_id'],
            week=item_data['week'],
            date=datetime.strptime(item_data['date'], '%Y-%m-%d').date(),
            is_repeat=item_data.get('is_repeat', False)
        )
        db.session.add(item)
    
    db.session.commit()
    
    return jsonify(schedule.to_dict()), 201


@bp.route('/schedules/<int:id>', methods=['DELETE'])
@login_required
def delete_schedule(id):
    """Delete a schedule."""
    schedule = Schedule.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(schedule)
    db.session.commit()
    return '', 204


@bp.route('/schedules/<int:id>/items/<int:item_id>/complete', methods=['POST'])
@login_required
def complete_schedule_item(id, item_id):
    """Mark a schedule item as completed."""
    schedule = Schedule.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    item = ScheduleItem.query.filter_by(id=item_id, schedule_id=schedule.id).first_or_404()
    
    item.completed = True
    item.completed_at = datetime.utcnow()
    
    # Also mark bottle as tasted if not already
    if item.bottle and not item.bottle.tasted:
        item.bottle.tasted = True
        item.bottle.tasting_date = datetime.utcnow().date()
    
    db.session.commit()
    
    return jsonify(item.to_dict())

