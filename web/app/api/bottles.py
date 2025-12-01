"""
Bottles API endpoints
"""

from flask import request, jsonify, current_app, send_from_directory
from app.api import bp
from app.models import Bottle
from app import db
from flask_login import login_required, current_user
from datetime import datetime
import os
from werkzeug.utils import secure_filename


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


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@bp.route('/bottles/<int:id>/photo', methods=['POST'])
@login_required
def upload_bottle_photo(id):
    """Upload a photo for a bottle."""
    bottle = Bottle.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    if 'photo' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['photo']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF'}), 400
    
    # Create uploads directory if it doesn't exist
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if isinstance(upload_folder, str):
        upload_folder = os.path.abspath(upload_folder)
    else:
        upload_folder = str(upload_folder)
    
    os.makedirs(upload_folder, exist_ok=True)
    
    # Create user-specific subdirectory
    user_upload_dir = os.path.join(upload_folder, str(current_user.id))
    os.makedirs(user_upload_dir, exist_ok=True)
    
    # Generate unique filename
    filename = secure_filename(file.filename)
    file_ext = filename.rsplit('.', 1)[1].lower()
    unique_filename = f"bottle_{bottle.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_ext}"
    filepath = os.path.join(user_upload_dir, unique_filename)
    
    # Save file
    file.save(filepath)
    
    # Delete old photo if exists
    if bottle.photo_path:
        old_path = os.path.join(upload_folder, bottle.photo_path)
        if os.path.exists(old_path):
            try:
                os.remove(old_path)
            except:
                pass  # Ignore errors deleting old file
    
    # Update bottle with new photo path (relative to upload folder)
    bottle.photo_path = os.path.join(str(current_user.id), unique_filename)
    bottle.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'success': True,
        'photo_path': bottle.photo_path,
        'photo_url': f'/api/bottles/{bottle.id}/photo'
    })


@bp.route('/bottles/<int:id>/photo', methods=['GET'])
@login_required
def get_bottle_photo(id):
    """Get bottle photo."""
    bottle = Bottle.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    if not bottle.photo_path:
        return jsonify({'error': 'No photo for this bottle'}), 404
    
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if isinstance(upload_folder, str):
        upload_folder = os.path.abspath(upload_folder)
    else:
        upload_folder = str(upload_folder)
    
    photo_path = os.path.join(upload_folder, bottle.photo_path)
    
    if not os.path.exists(photo_path):
        return jsonify({'error': 'Photo file not found'}), 404
    
    directory = os.path.dirname(photo_path)
    filename = os.path.basename(photo_path)
    
    return send_from_directory(directory, filename)


@bp.route('/bottles/<int:id>/photo', methods=['DELETE'])
@login_required
def delete_bottle_photo(id):
    """Delete bottle photo."""
    bottle = Bottle.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    if not bottle.photo_path:
        return jsonify({'error': 'No photo to delete'}), 404
    
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if isinstance(upload_folder, str):
        upload_folder = os.path.abspath(upload_folder)
    else:
        upload_folder = str(upload_folder)
    
    photo_path = os.path.join(upload_folder, bottle.photo_path)
    
    if os.path.exists(photo_path):
        try:
            os.remove(photo_path)
        except:
            pass  # Ignore errors
    
    bottle.photo_path = None
    bottle.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'success': True})

