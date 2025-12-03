"""
Admin catalog management API endpoints
Part of ENH-015: Catalog Management & Administration
"""

from flask import request, jsonify
from flask_login import login_required, current_user
from app.api import bp
from app.models import MasterBeverage, db
from sqlalchemy import func, or_, and_
from functools import wraps


def admin_required_api(f):
    """Decorator to require admin role for API endpoints."""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/admin/catalog/duplicates', methods=['GET'])
@admin_required_api
def find_duplicates():
    """Find duplicate catalog entries based on name and brand."""
    
    # Group by name and brand, find duplicates (database-agnostic)
    duplicates_query = db.session.query(
        MasterBeverage.name,
        MasterBeverage.brand,
        func.count(MasterBeverage.id).label('count')
    ).group_by(
        MasterBeverage.name,
        MasterBeverage.brand
    ).having(
        func.count(MasterBeverage.id) > 1
    ).all()
    
    duplicates = []
    for name, brand, count in duplicates_query:
        # Get all entries with this name and brand
        entries = MasterBeverage.query.filter_by(name=name, brand=brand).all()
        duplicates.append({
            'name': name,
            'brand': brand,
            'count': count,
            'entries': [e.to_dict() for e in entries]
        })
    
    return jsonify({
        'duplicates': duplicates,
        'total_groups': len(duplicates)
    })


@bp.route('/admin/catalog/<int:merge_from_id>/merge/<int:merge_to_id>', methods=['POST'])
@admin_required_api
def merge_entries(merge_from_id, merge_to_id):
    """Merge two catalog entries, keeping merge_to and deleting merge_from."""
    
    from_entry = MasterBeverage.query.get_or_404(merge_from_id)
    to_entry = MasterBeverage.query.get_or_404(merge_to_id)
    
    # Merge data - prefer non-null values from from_entry
    if not to_entry.brand and from_entry.brand:
        to_entry.brand = from_entry.brand
    if not to_entry.description and from_entry.description:
        to_entry.description = from_entry.description
    if not to_entry.abv and from_entry.abv:
        to_entry.abv = from_entry.abv
    if not to_entry.image_url and from_entry.image_url:
        to_entry.image_url = from_entry.image_url
    
    # Mark as verified if either was verified
    if from_entry.verified:
        to_entry.verified = True
    
    db.session.delete(from_entry)
    db.session.commit()
    
    return jsonify({
        'message': f'Successfully merged entry {merge_from_id} into {merge_to_id}',
        'merged_entry': to_entry.to_dict()
    })


@bp.route('/admin/catalog/analytics', methods=['GET'])
@admin_required_api
def catalog_analytics():
    """Get catalog analytics and statistics."""
    
    total_entries = MasterBeverage.query.count()
    verified_entries = MasterBeverage.query.filter_by(verified=True).count()
    unverified_entries = total_entries - verified_entries
    
    # Category distribution
    category_counts = db.session.query(
        MasterBeverage.category,
        func.count(MasterBeverage.id).label('count')
    ).group_by(MasterBeverage.category).all()
    
    categories = {cat: count for cat, count in category_counts}
    
    # Source distribution
    source_counts = db.session.query(
        MasterBeverage.source,
        func.count(MasterBeverage.id).label('count')
    ).group_by(MasterBeverage.source).all()
    
    sources = {src: count for src, count in source_counts if src}
    
    # Completeness metrics
    entries_with_images = MasterBeverage.query.filter(
        MasterBeverage.image_url.isnot(None)
    ).count()
    
    entries_with_descriptions = MasterBeverage.query.filter(
        MasterBeverage.description.isnot(None)
    ).count()
    
    entries_with_abv = MasterBeverage.query.filter(
        MasterBeverage.abv.isnot(None)
    ).count()
    
    return jsonify({
        'total_entries': total_entries,
        'verified_entries': verified_entries,
        'unverified_entries': unverified_entries,
        'verification_rate': round((verified_entries / total_entries * 100) if total_entries > 0 else 0, 2),
        'categories': categories,
        'sources': sources,
        'completeness': {
            'with_images': entries_with_images,
            'with_descriptions': entries_with_descriptions,
            'with_abv': entries_with_abv,
            'image_rate': round((entries_with_images / total_entries * 100) if total_entries > 0 else 0, 2),
            'description_rate': round((entries_with_descriptions / total_entries * 100) if total_entries > 0 else 0, 2),
            'abv_rate': round((entries_with_abv / total_entries * 100) if total_entries > 0 else 0, 2)
        }
    })


@bp.route('/admin/catalog/export', methods=['GET'])
@admin_required_api
def export_catalog():
    """Export entire catalog as JSON or CSV."""
    
    format_type = request.args.get('format', 'json').lower()
    
    all_beverages = MasterBeverage.query.order_by(MasterBeverage.name).all()
    
    if format_type == 'csv':
        import csv
        import io
        from flask import Response
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            'id', 'name', 'brand', 'category', 'subcategory', 'abv',
            'region', 'country', 'description', 'source', 'verified'
        ])
        writer.writeheader()
        
        for bev in all_beverages:
            writer.writerow({
                'id': bev.id,
                'name': bev.name,
                'brand': bev.brand or '',
                'category': bev.category,
                'subcategory': bev.subcategory or '',
                'abv': bev.abv or '',
                'region': bev.region or '',
                'country': bev.country or '',
                'description': bev.description or '',
                'source': bev.source or '',
                'verified': bev.verified
            })
        
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=catalog_export.csv'}
        )
    else:
        # JSON export
        return jsonify({
            'export_date': db.session.execute(db.text('SELECT NOW()')).scalar().isoformat(),
            'total_entries': len(all_beverages),
            'beverages': [b.to_dict() for b in all_beverages]
        })


@bp.route('/admin/catalog/bulk-verify', methods=['POST'])
@admin_required_api
def bulk_verify():
    """Bulk verify/unverify catalog entries."""
    
    data = request.get_json() or {}
    entry_ids = data.get('entry_ids', [])
    verified = data.get('verified', True)
    
    if not entry_ids:
        return jsonify({'error': 'No entry IDs provided'}), 400
    
    updated = MasterBeverage.query.filter(MasterBeverage.id.in_(entry_ids)).update(
        {MasterBeverage.verified: verified},
        synchronize_session=False
    )
    
    db.session.commit()
    
    return jsonify({
        'message': f'Updated {updated} entries',
        'verified': verified,
        'updated_count': updated
    })


@bp.route('/admin/catalog/<int:entry_id>/verify', methods=['POST'])
@admin_required_api
def verify_entry(entry_id):
    """Mark a catalog entry as verified."""
    
    entry = MasterBeverage.query.get_or_404(entry_id)
    entry.verified = True
    db.session.commit()
    
    return jsonify({
        'message': 'Entry verified',
        'entry': entry.to_dict()
    })

