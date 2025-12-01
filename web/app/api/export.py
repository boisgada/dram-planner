"""
Export/Import API endpoints
"""

from flask import request, jsonify, send_file, Response
from app.api import bp
from app.models import Bottle, Schedule, ScheduleItem
from app import db
from flask_login import login_required, current_user
from datetime import datetime
import json
import csv
import io
import sys
import os

# Simplified import functions for web application
def normalize_bottle_data(data):
    """Normalize bottle data to standard format."""
    normalized = {
        'name': str(data.get('name', '')).strip(),
        'category': str(data.get('category', 'other')).lower().strip(),
        'abv': data.get('abv'),
        'price_paid': data.get('price_paid'),
        'purchase_date': data.get('purchase_date'),
        'opened_date': data.get('opened_date'),
        'notes': str(data.get('notes', '')).strip(),
        'barcode': str(data.get('barcode', '')).strip(),
        'tasted': data.get('tasted', False),
        'tasting_date': data.get('tasting_date'),
        'rating': data.get('rating'),
        'tasting_notes': str(data.get('tasting_notes', '')).strip()
    }
    return normalized


def validate_bottle_data(data, index=0):
    """Validate bottle data."""
    errors = []
    
    if not data.get('name'):
        errors.append(f"Bottle {index}: Name is required")
    
    valid_categories = ['bourbon', 'scotch', 'irish', 'gin', 'vodka', 'rum', 'tequila', 'liqueur', 'other']
    if data.get('category') and data['category'] not in valid_categories:
        errors.append(f"Bottle {index}: Invalid category '{data['category']}'")
    
    if data.get('abv') is not None:
        try:
            abv = float(data['abv'])
            if abv < 0 or abv > 100:
                errors.append(f"Bottle {index}: ABV must be between 0 and 100")
        except (ValueError, TypeError):
            errors.append(f"Bottle {index}: Invalid ABV value")
    
    return len(errors) == 0, errors


def import_from_csv(csv_file, preview=False):
    """Import bottles from CSV file."""
    bottles = []
    errors = []
    warnings = []
    
    if not os.path.exists(csv_file):
        errors.append(f"CSV file not found: {csv_file}")
        return bottles, errors, warnings
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            # Try to detect delimiter
            sample = f.read(1024)
            f.seek(0)
            sniffer = csv.Sniffer()
            try:
                delimiter = sniffer.sniff(sample).delimiter
            except:
                delimiter = ','
            
            reader = csv.DictReader(f, delimiter=delimiter)
            
            for idx, row in enumerate(reader, start=1):
                normalized = normalize_bottle_data(row)
                is_valid, validation_errors = validate_bottle_data(normalized, idx)
                
                if is_valid:
                    bottles.append(normalized)
                else:
                    errors.extend(validation_errors)
    
    except Exception as e:
        errors.append(f"Error reading CSV: {str(e)}")
    
    return bottles, errors, warnings


def import_from_json(json_file, preview=False):
    """Import bottles from JSON file."""
    bottles = []
    errors = []
    warnings = []
    
    if not os.path.exists(json_file):
        errors.append(f"JSON file not found: {json_file}")
        return bottles, errors, warnings
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract bottles array
        if isinstance(data, list):
            bottles_data = data
        elif isinstance(data, dict):
            if 'bottles' in data:
                bottles_data = data['bottles']
            else:
                errors.append("JSON file must contain 'bottles' array or be an array of bottles")
                return bottles, errors, warnings
        else:
            errors.append("JSON file must be an object or array")
            return bottles, errors, warnings
        
        if not isinstance(bottles_data, list):
            errors.append("Bottles data must be an array")
            return bottles, errors, warnings
        
        # Process each bottle
        for idx, bottle_data in enumerate(bottles_data, start=1):
            if not isinstance(bottle_data, dict):
                errors.append(f"Bottle {idx}: Must be an object")
                continue
            
            normalized = normalize_bottle_data(bottle_data)
            is_valid, validation_errors = validate_bottle_data(normalized, idx)
            
            if is_valid:
                bottles.append(normalized)
            else:
                errors.extend(validation_errors)
    
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON: {str(e)}")
    except Exception as e:
        errors.append(f"Error reading JSON: {str(e)}")
    
    return bottles, errors, warnings


@bp.route('/export/bottles', methods=['GET'])
@login_required
def export_bottles():
    """Export bottles to CSV or JSON."""
    format_type = request.args.get('format', 'json').lower()
    
    bottles = Bottle.query.filter_by(user_id=current_user.id).order_by(Bottle.name).all()
    
    if format_type == 'csv':
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            'name', 'category', 'abv', 'price_paid', 'purchase_date', 
            'opened_date', 'notes', 'barcode', 'tasted', 'tasting_date', 
            'rating', 'tasting_notes'
        ])
        writer.writeheader()
        
        for bottle in bottles:
            writer.writerow({
                'name': bottle.name,
                'category': bottle.category,
                'abv': bottle.abv or '',
                'price_paid': bottle.price_paid or '',
                'purchase_date': bottle.purchase_date.isoformat() if bottle.purchase_date else '',
                'opened_date': bottle.opened_date.isoformat() if bottle.opened_date else '',
                'notes': bottle.notes or '',
                'barcode': bottle.barcode or '',
                'tasted': 'true' if bottle.tasted else 'false',
                'tasting_date': bottle.tasting_date.isoformat() if bottle.tasting_date else '',
                'rating': bottle.rating or '',
                'tasting_notes': bottle.tasting_notes or ''
            })
        
        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename=dram-planner-collection-{datetime.now().strftime("%Y%m%d")}.csv'}
        )
    
    else:  # JSON
        bottles_data = {
            'bottles': [bottle.to_dict() for bottle in bottles],
            'exported_at': datetime.utcnow().isoformat(),
            'total': len(bottles)
        }
        
        output = io.StringIO()
        json.dump(bottles_data, output, indent=2, default=str)
        output.seek(0)
        
        return Response(
            output.getvalue(),
            mimetype='application/json',
            headers={'Content-Disposition': f'attachment; filename=dram-planner-collection-{datetime.now().strftime("%Y%m%d")}.json'}
        )


@bp.route('/export/schedule/<int:schedule_id>', methods=['GET'])
@login_required
def export_schedule_ical(schedule_id):
    """Export schedule to iCal format."""
    schedule = Schedule.query.filter_by(id=schedule_id, user_id=current_user.id).first_or_404()
    
    # Generate iCal content
    ical_lines = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//Dram Planner//EN',
        'CALSCALE:GREGORIAN',
        'METHOD:PUBLISH',
        f'X-WR-CALNAME:{schedule.name}',
        'X-WR-TIMEZONE:UTC',
    ]
    
    # Add each schedule item as an event
    for item in schedule.items.order_by(ScheduleItem.date):
        if item.bottle:
            summary = f"Taste: {item.bottle.name}"
            description = f"Category: {item.bottle.category}"
            if item.bottle.abv:
                description += f"\\nABV: {item.bottle.abv}%"
            if item.bottle.notes:
                description += f"\\nNotes: {item.bottle.notes}"
            
            # Format date for iCal (YYYYMMDD)
            date_str = item.date.strftime('%Y%m%d')
            
            ical_lines.extend([
                'BEGIN:VEVENT',
                f'UID:dram-planner-{schedule.id}-{item.id}@dram-planner',
                f'DTSTART;VALUE=DATE:{date_str}',
                f'DTEND;VALUE=DATE:{date_str}',
                f'SUMMARY:{summary}',
                f'DESCRIPTION:{description}',
                f'STATUS:{"CONFIRMED" if item.completed else "TENTATIVE"}',
                'END:VEVENT'
            ])
    
    ical_lines.append('END:VCALENDAR')
    
    ical_content = '\r\n'.join(ical_lines)
    
    return Response(
        ical_content,
        mimetype='text/calendar',
        headers={'Content-Disposition': f'attachment; filename=dram-planner-schedule-{schedule.id}-{datetime.now().strftime("%Y%m%d")}.ics'}
    )


@bp.route('/import/bottles', methods=['POST'])
@login_required
def import_bottles():
    """Import bottles from CSV or JSON file."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    format_type = request.form.get('format', 'auto').lower()
    preview = request.form.get('preview', 'false').lower() == 'true'
    
    # Determine format from filename if auto
    if format_type == 'auto':
        if file.filename.endswith('.csv'):
            format_type = 'csv'
        elif file.filename.endswith('.json'):
            format_type = 'json'
        else:
            return jsonify({'error': 'Unsupported file format. Use CSV or JSON.'}), 400
    
    # Save uploaded file temporarily
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
        file.save(tmp_file.name)
        tmp_path = tmp_file.name
    
    try:
        # Import based on format
        if format_type == 'csv':
            if import_from_csv:
                bottles, errors, warnings = import_from_csv(tmp_path, preview=preview)
            else:
                return jsonify({'error': 'CSV import not available'}), 500
        elif format_type == 'json':
            if import_from_json:
                bottles, errors, warnings = import_from_json(tmp_path, preview=preview)
            else:
                return jsonify({'error': 'JSON import not available'}), 500
        else:
            return jsonify({'error': 'Unsupported format'}), 400
        
        # If preview, return preview data
        if preview:
            return jsonify({
                'preview': True,
                'bottles': bottles[:10],  # First 10 for preview
                'total': len(bottles),
                'errors': errors,
                'warnings': warnings
            })
        
        # If not preview, import bottles
        if errors:
            return jsonify({
                'error': 'Import validation failed',
                'errors': errors,
                'warnings': warnings
            }), 400
        
        imported_count = 0
        for bottle_data in bottles:
            # Check if bottle already exists (by name)
            existing = Bottle.query.filter_by(
                user_id=current_user.id,
                name=bottle_data['name']
            ).first()
            
            if existing:
                continue  # Skip duplicates
            
            bottle = Bottle(
                user_id=current_user.id,
                name=bottle_data['name'],
                category=bottle_data.get('category', 'other').lower(),
                abv=float(bottle_data.get('abv', 0)) if bottle_data.get('abv') else 0.0,
                price_paid=float(bottle_data.get('price_paid', 0)) if bottle_data.get('price_paid') else 0.0,
                purchase_date=datetime.strptime(bottle_data['purchase_date'], '%Y-%m-%d').date() if bottle_data.get('purchase_date') else None,
                notes=bottle_data.get('notes', ''),
                barcode=bottle_data.get('barcode', '')
            )
            
            db.session.add(bottle)
            imported_count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'imported': imported_count,
            'total': len(bottles),
            'warnings': warnings
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Import failed: {str(e)}'}), 500
    
    finally:
        # Clean up temp file
        try:
            os.unlink(tmp_path)
        except:
            pass

