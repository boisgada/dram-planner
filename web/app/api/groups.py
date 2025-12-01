"""
Groups API endpoints for Dram Planner Web
"""

from flask import request, jsonify
from app.api import bp
from app.models import UserGroup, GroupMembership, GroupSchedule, GroupScheduleItem, User, db
from flask_login import login_required, current_user
from datetime import datetime
import sys
import os

# Add parent directory to path to import CLI modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

# Try to import schedule generator
try:
    import schedule_generator
except ImportError:
    schedule_generator = None


@bp.route('/groups', methods=['GET'])
@login_required
def get_groups():
    """Get all groups the current user is a member of."""

    memberships = GroupMembership.query.filter_by(user_id=current_user.id).all()
    group_ids = [m.group_id for m in memberships]

    groups = UserGroup.query.filter(UserGroup.id.in_(group_ids)).all()

    return jsonify({
        'groups': [group.to_dict() for group in groups]
    })


@bp.route('/groups', methods=['POST'])
@login_required
def create_group():
    """Create a new group."""

    data = request.get_json() or {}

    if not data.get('name'):
        return jsonify({'error': 'Group name is required'}), 400

    group = UserGroup(
        name=data['name'].strip(),
        description=data.get('description', '').strip(),
        is_private=data.get('is_private', False),
        created_by_id=current_user.id
    )

    db.session.add(group)
    db.session.commit()

    # Add creator as admin member
    membership = GroupMembership(
        user_id=current_user.id,
        group_id=group.id,
        role='admin'
    )
    db.session.add(membership)
    db.session.commit()

    return jsonify(group.to_dict()), 201


@bp.route('/groups/<int:group_id>', methods=['GET'])
@login_required
def get_group(group_id):
    """Get a specific group."""

    # Check if user is a member
    membership = GroupMembership.query.filter_by(
        user_id=current_user.id,
        group_id=group_id
    ).first()

    if not membership:
        return jsonify({'error': 'Not a member of this group'}), 403

    group = UserGroup.query.get_or_404(group_id)

    return jsonify(group.to_dict())


@bp.route('/groups/<int:group_id>', methods=['PUT'])
@login_required
def update_group(group_id):
    """Update a group (admin only)."""

    # Check if user is admin
    membership = GroupMembership.query.filter_by(
        user_id=current_user.id,
        group_id=group_id,
        role='admin'
    ).first()

    if not membership:
        return jsonify({'error': 'Admin access required'}), 403

    group = UserGroup.query.get_or_404(group_id)
    data = request.get_json() or {}

    if 'name' in data:
        group.name = data['name'].strip()
    if 'description' in data:
        group.description = data['description'].strip()
    if 'is_private' in data:
        group.is_private = data['is_private']

    db.session.commit()

    return jsonify(group.to_dict())


@bp.route('/groups/<int:group_id>', methods=['DELETE'])
@login_required
def delete_group(group_id):
    """Delete a group (admin only)."""

    # Check if user is admin
    membership = GroupMembership.query.filter_by(
        user_id=current_user.id,
        group_id=group_id,
        role='admin'
    ).first()

    if not membership:
        return jsonify({'error': 'Admin access required'}), 403

    group = UserGroup.query.get_or_404(group_id)

    db.session.delete(group)
    db.session.commit()

    return jsonify({'message': 'Group deleted'})


@bp.route('/groups/<int:group_id>/members', methods=['GET'])
@login_required
def get_group_members(group_id):
    """Get group members."""

    # Check if user is a member
    membership = GroupMembership.query.filter_by(
        user_id=current_user.id,
        group_id=group_id
    ).first()

    if not membership:
        return jsonify({'error': 'Not a member of this group'}), 403

    members = GroupMembership.query.filter_by(group_id=group_id).all()

    member_data = []
    for member in members:
        member_data.append({
            'user_id': member.user_id,
            'username': member.user.username,
            'role': member.role,
            'joined_at': member.joined_at.isoformat()
        })

    return jsonify({'members': member_data})


@bp.route('/groups/<int:group_id>/members', methods=['POST'])
@login_required
def add_group_member(group_id):
    """Add a member to the group (admin only)."""

    # Check if user is admin
    membership = GroupMembership.query.filter_by(
        user_id=current_user.id,
        group_id=group_id,
        role='admin'
    ).first()

    if not membership:
        return jsonify({'error': 'Admin access required'}), 403

    data = request.get_json() or {}

    if not data.get('username'):
        return jsonify({'error': 'Username is required'}), 400

    # Find user
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Check if already a member
    existing = GroupMembership.query.filter_by(
        user_id=user.id,
        group_id=group_id
    ).first()

    if existing:
        return jsonify({'error': 'User is already a member'}), 400

    # Add membership
    new_membership = GroupMembership(
        user_id=user.id,
        group_id=group_id,
        role=data.get('role', 'member')
    )

    db.session.add(new_membership)
    db.session.commit()

    return jsonify({
        'user_id': user.id,
        'username': user.username,
        'role': new_membership.role,
        'joined_at': new_membership.joined_at.isoformat()
    }), 201


@bp.route('/groups/<int:group_id>/members/<int:user_id>', methods=['DELETE'])
@login_required
def remove_group_member(group_id, user_id):
    """Remove a member from the group."""

    # Check permissions (admin or self)
    membership = GroupMembership.query.filter_by(
        user_id=current_user.id,
        group_id=group_id
    ).first()

    if not membership or (membership.role != 'admin' and current_user.id != user_id):
        return jsonify({'error': 'Permission denied'}), 403

    # Can't remove the last admin
    if membership.role == 'admin':
        admin_count = GroupMembership.query.filter_by(
            group_id=group_id,
            role='admin'
        ).count()
        if admin_count <= 1:
            return jsonify({'error': 'Cannot remove the last admin'}), 400

    member = GroupMembership.query.filter_by(
        user_id=user_id,
        group_id=group_id
    ).first_or_404()

    db.session.delete(member)
    db.session.commit()

    return jsonify({'message': 'Member removed'})


@bp.route('/groups/<int:group_id>/schedules', methods=['GET'])
@login_required
def get_group_schedules(group_id):
    """Get schedules for a group."""

    # Check if user is a member
    membership = GroupMembership.query.filter_by(
        user_id=current_user.id,
        group_id=group_id
    ).first()

    if not membership:
        return jsonify({'error': 'Not a member of this group'}), 403

    schedules = GroupSchedule.query.filter_by(group_id=group_id).order_by(
        GroupSchedule.created_at.desc()
    ).all()

    return jsonify({
        'schedules': [schedule.to_dict() for schedule in schedules]
    })


@bp.route('/groups/<int:group_id>/schedules', methods=['POST'])
@login_required
def create_group_schedule(group_id):
    """Create a schedule for a group."""

    # Check if user is a member
    membership = GroupMembership.query.filter_by(
        user_id=current_user.id,
        group_id=group_id
    ).first()

    if not membership:
        return jsonify({'error': 'Not a member of this group'}), 403

    data = request.get_json() or {}

    if not data.get('name'):
        return jsonify({'error': 'Schedule name is required'}), 400

    if not data.get('start_date'):
        return jsonify({'error': 'Start date is required'}), 400

    schedule = GroupSchedule(
        group_id=group_id,
        name=data['name'].strip(),
        description=data.get('description', '').strip(),
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
        weeks=data.get('weeks', 52),
        created_by_id=current_user.id
    )

    db.session.add(schedule)
    db.session.commit()

    # Generate schedule items based on group members' collections
    _generate_group_schedule_items(schedule, data.get('bottles', []))

    return jsonify(schedule.to_dict()), 201


def _generate_group_schedule_items(schedule, bottle_list=None):
    """Generate schedule items for a group schedule."""
    # This is a simplified version - in practice, you'd want to
    # aggregate bottles from all group members and create a collaborative schedule

    if not bottle_list:
        # For now, create placeholder items
        # TODO: Implement proper group bottle aggregation
        bottle_list = [
            {'name': 'Group Selection 1', 'category': 'whiskey'},
            {'name': 'Group Selection 2', 'category': 'scotch'},
            {'name': 'Group Selection 3', 'category': 'bourbon'},
        ]

    current_date = schedule.start_date
    for week in range(1, schedule.weeks + 1):
        bottle = bottle_list[(week - 1) % len(bottle_list)]

        item = GroupScheduleItem(
            schedule_id=schedule.id,
            week=week,
            tasting_date=current_date,
            bottle_name=bottle['name'],
            category=bottle.get('category', 'other')
        )

        db.session.add(item)
        current_date = current_date.replace(day=current_date.day + 7)  # Add 7 days

    db.session.commit()


@bp.route('/groups/<int:group_id>/schedules/<int:schedule_id>', methods=['GET'])
@login_required
def get_group_schedule(group_id, schedule_id):
    """Get a specific group schedule."""

    # Check if user is a member
    membership = GroupMembership.query.filter_by(
        user_id=current_user.id,
        group_id=group_id
    ).first()

    if not membership:
        return jsonify({'error': 'Not a member of this group'}), 403

    schedule = GroupSchedule.query.filter_by(
        id=schedule_id,
        group_id=group_id
    ).first_or_404()

    return jsonify(schedule.to_dict())


@bp.route('/groups/<int:group_id>/schedules/<int:schedule_id>/items', methods=['GET'])
@login_required
def get_group_schedule_items(group_id, schedule_id):
    """Get items for a group schedule."""

    # Check if user is a member
    membership = GroupMembership.query.filter_by(
        user_id=current_user.id,
        group_id=group_id
    ).first()

    if not membership:
        return jsonify({'error': 'Not a member of this group'}), 403

    items = GroupScheduleItem.query.filter_by(schedule_id=schedule_id).order_by(
        GroupScheduleItem.week
    ).all()

    return jsonify({
        'items': [item.to_dict() for item in items]
    })


@bp.route('/groups/<int:group_id>/schedules/<int:schedule_id>/items/<int:item_id>/complete', methods=['POST'])
@login_required
def complete_group_schedule_item(group_id, schedule_id, item_id):
    """Mark a group schedule item as completed."""

    # Check if user is a member
    membership = GroupMembership.query.filter_by(
        user_id=current_user.id,
        group_id=group_id
    ).first()

    if not membership:
        return jsonify({'error': 'Not a member of this group'}), 403

    item = GroupScheduleItem.query.filter_by(
        id=item_id,
        schedule_id=schedule_id
    ).first_or_404()

    if item.completed:
        return jsonify({'error': 'Item already completed'}), 400

    item.completed = True
    item.completed_by_id = current_user.id
    item.completed_at = datetime.utcnow()

    db.session.commit()

    return jsonify(item.to_dict())
