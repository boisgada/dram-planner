"""
Master Beverage Catalog API endpoints
"""

from flask import request, jsonify
from app.api import bp
from app.models import MasterBeverage, db
from flask_login import login_required, current_user
from sqlalchemy import or_, and_
import json
import csv
import io


@bp.route('/catalog/search', methods=['GET'])
@login_required
def search_catalog():
    """Search the master beverage catalog."""

    query = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    brand = request.args.get('brand', '').strip()
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))

    # Build the query
    q = MasterBeverage.query

    if query:
        # Search in name, brand, and description
        search_term = f'%{query}%'
        q = q.filter(or_(
            MasterBeverage.name.ilike(search_term),
            MasterBeverage.brand.ilike(search_term),
            MasterBeverage.description.ilike(search_term)
        ))

    if category:
        q = q.filter(MasterBeverage.category == category)

    if brand:
        q = q.filter(MasterBeverage.brand.ilike(f'%{brand}%'))

    # Order by name
    q = q.order_by(MasterBeverage.name)

    # Get total count
    total = q.count()

    # Apply pagination
    beverages = q.offset(offset).limit(limit).all()

    return jsonify({
        'beverages': [b.to_dict() for b in beverages],
        'total': total,
        'limit': limit,
        'offset': offset
    })


@bp.route('/catalog/categories', methods=['GET'])
@login_required
def get_catalog_categories():
    """Get all unique categories in the catalog."""

    categories = db.session.query(MasterBeverage.category).distinct().order_by(MasterBeverage.category).all()

    return jsonify({
        'categories': [cat[0] for cat in categories]
    })


@bp.route('/catalog/brands', methods=['GET'])
@login_required
def get_catalog_brands():
    """Get all unique brands in the catalog."""

    brands = db.session.query(MasterBeverage.brand).distinct().filter(
        MasterBeverage.brand.isnot(None)
    ).order_by(MasterBeverage.brand).all()

    return jsonify({
        'brands': [brand[0] for brand in brands if brand[0]]
    })


@bp.route('/catalog/<int:id>', methods=['GET'])
@login_required
def get_catalog_beverage(id):
    """Get a specific beverage from the catalog."""

    beverage = MasterBeverage.query.get_or_404(id)

    return jsonify(beverage.to_dict())


@bp.route('/catalog', methods=['POST'])
@login_required
def add_catalog_beverage():
    """Add a new beverage to the catalog (admin functionality)."""

    # Admin permission check
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    
    data = request.get_json() or {}

    if not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400

    beverage = MasterBeverage(
        name=data['name'].strip(),
        brand=data.get('brand', '').strip() or None,
        category=data.get('category', 'other'),
        subcategory=data.get('subcategory', '').strip() or None,
        abv=float(data['abv']) if data.get('abv') else None,
        region=data.get('region', '').strip() or None,
        country=data.get('country', '').strip() or None,
        description=data.get('description', '').strip() or None,
        tasting_notes=data.get('tasting_notes', '').strip() or None,
        image_url=data.get('image_url', '').strip() or None,
        external_id=data.get('external_id', '').strip() or None,
        source=data.get('source', 'internal'),
        verified=data.get('verified', False)
    )

    db.session.add(beverage)
    db.session.commit()

    return jsonify(beverage.to_dict()), 201


@bp.route('/catalog/<int:id>', methods=['PUT'])
@login_required
def update_catalog_beverage(id):
    """Update a beverage in the catalog (admin functionality)."""

    # Admin permission check
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    
    beverage = MasterBeverage.query.get_or_404(id)
    data = request.get_json() or {}

    if 'name' in data:
        beverage.name = data['name'].strip()
    if 'brand' in data:
        beverage.brand = data['brand'].strip() if data['brand'] else None
    if 'category' in data:
        beverage.category = data['category']
    if 'subcategory' in data:
        beverage.subcategory = data['subcategory'].strip() if data['subcategory'] else None
    if 'abv' in data:
        beverage.abv = float(data['abv']) if data['abv'] else None
    if 'region' in data:
        beverage.region = data['region'].strip() if data['region'] else None
    if 'country' in data:
        beverage.country = data['country'].strip() if data['country'] else None
    if 'description' in data:
        beverage.description = data['description'].strip() if data['description'] else None
    if 'tasting_notes' in data:
        beverage.tasting_notes = data['tasting_notes'].strip() if data['tasting_notes'] else None
    if 'image_url' in data:
        beverage.image_url = data['image_url'].strip() if data['image_url'] else None
    if 'external_id' in data:
        beverage.external_id = data['external_id'].strip() if data['external_id'] else None
    if 'source' in data:
        beverage.source = data['source']
    if 'verified' in data:
        beverage.verified = data['verified']

    db.session.commit()

    return jsonify(beverage.to_dict())


@bp.route('/catalog/<int:id>', methods=['DELETE'])
@login_required
def delete_catalog_beverage(id):
    """Delete a beverage from the catalog (admin functionality)."""

    # Admin permission check
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    
    beverage = MasterBeverage.query.get_or_404(id)

    db.session.delete(beverage)
    db.session.commit()

    return jsonify({'message': 'Beverage deleted from catalog'})


@bp.route('/catalog/populate-sample', methods=['POST'])
@login_required
def populate_sample_catalog():
    """Populate the catalog with sample data (development only)."""

    # TODO: Remove this endpoint in production
    sample_beverages = [
        {
            'name': 'Buffalo Trace Kentucky Straight Bourbon',
            'brand': 'Buffalo Trace',
            'category': 'bourbon',
            'abv': 45.0,
            'region': 'Kentucky',
            'country': 'USA',
            'description': 'A well-balanced bourbon with notes of vanilla, caramel, and oak.',
            'source': 'internal',
            'verified': True
        },
        {
            'name': 'Macallan 12 Year Old Sherry Oak',
            'brand': 'Macallan',
            'category': 'scotch',
            'abv': 43.0,
            'region': 'Speyside',
            'country': 'Scotland',
            'description': 'Rich sherry influence with dried fruits and spice notes.',
            'source': 'internal',
            'verified': True
        },
        {
            'name': 'Jameson Irish Whiskey',
            'brand': 'Jameson',
            'category': 'irish',
            'abv': 40.0,
            'region': 'Dublin',
            'country': 'Ireland',
            'description': 'Triple distilled for smoothness with vanilla and spice.',
            'source': 'internal',
            'verified': True
        },
        {
            'name': 'Hendrick\'s Gin',
            'brand': 'Hendrick\'s',
            'category': 'clear',
            'abv': 41.4,
            'region': 'Scotland',
            'country': 'Scotland',
            'description': 'Unique gin with cucumber and rose petals.',
            'source': 'internal',
            'verified': True
        }
    ]

    added_count = 0
    for bev_data in sample_beverages:
        # Check if it already exists
        existing = MasterBeverage.query.filter_by(
            name=bev_data['name'],
            brand=bev_data['brand']
        ).first()

        if not existing:
            beverage = MasterBeverage(**bev_data)
            db.session.add(beverage)
            added_count += 1

    db.session.commit()

    return jsonify({
        'message': f'Added {added_count} sample beverages to catalog',
        'total_added': added_count
    })


@bp.route('/catalog/import', methods=['POST'])
@login_required
def import_catalog():
    """Import beverages from CSV or JSON file."""

    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    format_type = request.form.get('format', 'auto').lower()

    # Determine format from filename if auto
    if format_type == 'auto':
        if file.filename.endswith('.csv'):
            format_type = 'csv'
        elif file.filename.endswith('.json'):
            format_type = 'json'
        else:
            return jsonify({'error': 'Unsupported file format. Use CSV or JSON.'}), 400

    try:
        if format_type == 'csv':
            beverages_data = _parse_csv_import(file)
        elif format_type == 'json':
            beverages_data = _parse_json_import(file)
        else:
            return jsonify({'error': 'Unsupported format'}), 400

        # Validate and import
        imported_count = 0
        errors = []

        for i, bev_data in enumerate(beverages_data):
            try:
                # Validate required fields
                if not bev_data.get('name'):
                    errors.append(f'Row {i+1}: Missing name')
                    continue

                # Check if it already exists
                existing = MasterBeverage.query.filter_by(
                    name=bev_data['name'],
                    brand=bev_data.get('brand')
                ).first()

                if existing:
                    continue  # Skip duplicates

                # Create new beverage
                beverage = MasterBeverage(
                    name=bev_data['name'].strip(),
                    brand=bev_data.get('brand', '').strip() or None,
                    category=bev_data.get('category', 'other'),
                    subcategory=bev_data.get('subcategory', '').strip() or None,
                    abv=float(bev_data['abv']) if bev_data.get('abv') else None,
                    region=bev_data.get('region', '').strip() or None,
                    country=bev_data.get('country', '').strip() or None,
                    description=bev_data.get('description', '').strip() or None,
                    tasting_notes=bev_data.get('tasting_notes', '').strip() or None,
                    image_url=bev_data.get('image_url', '').strip() or None,
                    external_id=bev_data.get('external_id', '').strip() or None,
                    source=bev_data.get('source', 'imported'),
                    verified=bev_data.get('verified', False)
                )

                db.session.add(beverage)
                imported_count += 1

            except Exception as e:
                errors.append(f'Row {i+1}: {str(e)}')

        db.session.commit()

        result = {
            'message': f'Successfully imported {imported_count} beverages',
            'imported': imported_count
        }

        if errors:
            result['errors'] = errors
            result['message'] += f', {len(errors)} errors'

        return jsonify(result), 200 if not errors else 207  # 207 = Multi-Status

    except Exception as e:
        return jsonify({'error': f'Import failed: {str(e)}'}), 500


def _parse_csv_import(file):
    """Parse CSV file for beverage import."""
    content = file.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(content))

    beverages = []
    for row in reader:
        # Clean up the data
        beverage = {}
        for key, value in row.items():
            key = key.lower().strip()
            value = value.strip() if value else None

            # Map common column names
            if key in ['name', 'product_name', 'beverage_name']:
                beverage['name'] = value
            elif key in ['brand', 'brand_name', 'manufacturer']:
                beverage['brand'] = value
            elif key in ['category', 'type', 'spirit_type']:
                beverage['category'] = value
            elif key == 'subcategory':
                beverage['subcategory'] = value
            elif key in ['abv', 'alcohol', 'alcohol_content']:
                try:
                    beverage['abv'] = float(value) if value else None
                except ValueError:
                    beverage['abv'] = None
            elif key in ['region', 'origin_region']:
                beverage['region'] = value
            elif key in ['country', 'origin_country']:
                beverage['country'] = value
            elif key in ['description', 'desc', 'notes']:
                beverage['description'] = value
            elif key in ['tasting_notes', 'tasting']:
                beverage['tasting_notes'] = value
            elif key in ['image_url', 'image', 'photo']:
                beverage['image_url'] = value
            elif key == 'external_id':
                beverage['external_id'] = value
            elif key == 'source':
                beverage['source'] = value
            elif key == 'verified':
                beverage['verified'] = value.lower() in ['true', '1', 'yes'] if value else False

        if beverage.get('name'):  # Only add if name exists
            beverages.append(beverage)

    return beverages


def _parse_json_import(file):
    """Parse JSON file for beverage import."""
    content = file.read().decode('utf-8')
    data = json.loads(content)

    # Handle different JSON structures
    if isinstance(data, list):
        beverages = data
    elif isinstance(data, dict) and 'beverages' in data:
        beverages = data['beverages']
    elif isinstance(data, dict) and 'data' in data:
        beverages = data['data']
    else:
        beverages = [data]

    # Normalize field names
    normalized_beverages = []
    for bev in beverages:
        normalized = {}
        for key, value in bev.items():
            key = key.lower().replace('_', '').replace(' ', '')
            if key in ['name', 'productname', 'beveragename']:
                normalized['name'] = value
            elif key in ['brand', 'brandname', 'manufacturer']:
                normalized['brand'] = value
            elif key in ['category', 'type', 'spirittype']:
                normalized['category'] = value
            elif key == 'subcategory':
                normalized['subcategory'] = value
            elif key in ['abv', 'alcohol', 'alcoholcontent']:
                normalized['abv'] = value
            elif key in ['region', 'originregion']:
                normalized['region'] = value
            elif key in ['country', 'origincountry']:
                normalized['country'] = value
            elif key in ['description', 'desc', 'notes']:
                normalized['description'] = value
            elif key in ['tastingnotes', 'tasting']:
                normalized['tasting_notes'] = value
            elif key in ['imageurl', 'image', 'photo']:
                normalized['image_url'] = value
            elif key == 'externalid':
                normalized['external_id'] = value
            elif key == 'source':
                normalized['source'] = value
            elif key == 'verified':
                normalized['verified'] = value

        if normalized.get('name'):
            normalized_beverages.append(normalized)

    return normalized_beverages
