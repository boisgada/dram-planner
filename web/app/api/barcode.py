"""
Barcode API endpoints for Dram Planner Web
"""

from flask import request, jsonify
from app.api import bp
from flask_login import login_required, current_user
import requests
import json
import sys
import os

# Add parent directory to path to import CLI modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

# Try to import barcode_lookup module
try:
    import barcode_lookup
    BARCODE_AVAILABLE = True
except ImportError:
    BARCODE_AVAILABLE = False
    barcode_lookup = None


@bp.route('/barcode/lookup/<barcode>', methods=['GET'])
@login_required
def lookup_barcode(barcode):
    """Look up product information from Open Food Facts API."""

    if not BARCODE_AVAILABLE:
        return jsonify({
            'error': 'Barcode lookup not available. Missing barcode_lookup module.'
        }), 503

    if not barcode or not barcode.strip():
        return jsonify({'error': 'Barcode is required'}), 400

    try:
        # Use the existing barcode_lookup module
        product = barcode_lookup.lookup_barcode(barcode.strip())

        if not product:
            return jsonify({
                'error': 'Product not found for this barcode',
                'barcode': barcode
            }), 404

        # Format for web UI
        formatted_product = {
            'name': product.get('name', ''),
            'brand': product.get('brand', ''),
            'category': product.get('category', 'other'),
            'abv': product.get('abv'),
            'volume': product.get('volume', ''),
            'description': product.get('description', ''),
            'image_url': product.get('image_url', ''),
            'barcode': product.get('barcode', barcode),
            'source': product.get('source', 'openfoodfacts')
        }

        return jsonify({
            'success': True,
            'product': formatted_product
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': f'Network error connecting to barcode service: {str(e)}',
            'barcode': barcode
        }), 503

    except Exception as e:
        return jsonify({
            'error': f'Error looking up barcode: {str(e)}',
            'barcode': barcode
        }), 500


@bp.route('/barcode/categories', methods=['GET'])
@login_required
def get_barcode_categories():
    """Get list of supported barcode categories."""

    categories = [
        'bourbon', 'scotch', 'irish', 'clear', 'liqueur', 'other'
    ]

    return jsonify({
        'categories': categories
    })
