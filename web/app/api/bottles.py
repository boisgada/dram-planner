"""
Bottles API endpoints
"""

from flask import request, jsonify
from app.api import bp
from app.models import Bottle
from app import db
from flask_login import login_required, current_user
from datetime import datetime


@bp.route('/bottles', methods=['GET'])
@login_required
def get_bottles():
    """Get all bottles for current user."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category')
    tasted = request.args.get('tasted')
    search = request.args.get('search')
    
    query = Bottle.query.filter_by(user_id=current_user.id)
    
    if category:
        query = query.filter_by(category=category.lower())
    if tasted is not None:
        query = query.filter_by(tasted=tasted.lower() == 'true')
    if search:
        query = query.filter(Bottle.name.ilike(f'%{search}%'))
    
    pagination = query.order_by(Bottle.name).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'bottles': [bottle.to_dict() for bottle in pagination.items],
        'pagination': {
            'page': page,
            'pages': pagination.pages,
            'per_page': per_page,
            'total': pagination.total
        }
    })


@bp.route('/bottles/<int:id>', methods=['GET'])
@login_required
def get_bottle(id):
    """Get a specific bottle."""
    bottle = Bottle.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    return jsonify(bottle.to_dict())


@bp.route('/bottles', methods=['POST'])
@login_required
def create_bottle():
    """Create a new bottle."""
    data = request.get_json() or {}
    
    bottle = Bottle(
        user_id=current_user.id,
        name=data.get('name', '').strip(),
        category=data.get('category', 'other').lower(),
        abv=float(data.get('abv', 0)) if data.get('abv') else 0.0,
        price_paid=float(data.get('price_paid', 0)) if data.get('price_paid') else 0.0,
        purchase_date=datetime.strptime(data['purchase_date'], '%Y-%m-%d').date() if data.get('purchase_date') else None,
        notes=data.get('notes', ''),
        barcode=data.get('barcode', '')
    )
    
    if not bottle.name:
        return jsonify({'error': 'Name is required'}), 400
    
    db.session.add(bottle)
    db.session.commit()
    
    return jsonify(bottle.to_dict()), 201


@bp.route('/bottles/<int:id>', methods=['PUT'])
@login_required
def update_bottle(id):
    """Update a bottle."""
    bottle = Bottle.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    data = request.get_json() or {}
    
    if 'name' in data:
        bottle.name = data['name'].strip()
    if 'category' in data:
        bottle.category = data['category'].lower()
    if 'abv' in data:
        bottle.abv = float(data['abv']) if data['abv'] else 0.0
    if 'price_paid' in data:
        bottle.price_paid = float(data['price_paid']) if data['price_paid'] else 0.0
    if 'purchase_date' in data:
        bottle.purchase_date = datetime.strptime(data['purchase_date'], '%Y-%m-%d').date() if data['purchase_date'] else None
    if 'notes' in data:
        bottle.notes = data['notes']
    if 'barcode' in data:
        bottle.barcode = data['barcode']
    
    bottle.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(bottle.to_dict())


@bp.route('/bottles/<int:id>', methods=['DELETE'])
@login_required
def delete_bottle(id):
    """Delete a bottle."""
    bottle = Bottle.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(bottle)
    db.session.commit()
    return '', 204


@bp.route('/bottles/<int:id>/tasting', methods=['POST'])
@login_required
def record_tasting(id):
    """Record a tasting for a bottle."""
    bottle = Bottle.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    data = request.get_json() or {}
    
    bottle.tasted = True
    bottle.tasting_date = datetime.strptime(data['tasting_date'], '%Y-%m-%d').date() if data.get('tasting_date') else datetime.utcnow().date()
    bottle.rating = float(data['rating']) if data.get('rating') else None
    bottle.tasting_notes = data.get('tasting_notes', '')
    
    if not bottle.opened_date:
        bottle.opened_date = bottle.tasting_date
    
    bottle.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(bottle.to_dict())


@bp.route('/bottles/stats', methods=['GET'])
@login_required
def get_stats():
    """Get collection statistics."""
    total = Bottle.query.filter_by(user_id=current_user.id).count()
    tasted = Bottle.query.filter_by(user_id=current_user.id, tasted=True).count()
    untasted = total - tasted
    
    # By category
    from sqlalchemy import func
    category_stats = db.session.query(
        Bottle.category,
        func.count(Bottle.id).label('count'),
        func.sum(func.cast(Bottle.tasted, db.Integer)).label('tasted')
    ).filter_by(user_id=current_user.id).group_by(Bottle.category).all()
    
    categories = {cat: {'total': count, 'tasted': tasted_count} 
                  for cat, count, tasted_count in category_stats}
    
    # Average rating
    avg_rating = db.session.query(func.avg(Bottle.rating)).filter_by(
        user_id=current_user.id, tasted=True
    ).scalar() or 0
    
    return jsonify({
        'total': total,
        'tasted': tasted,
        'untasted': untasted,
        'categories': categories,
        'average_rating': float(avg_rating) if avg_rating else None
    })

