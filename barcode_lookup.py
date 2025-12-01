#!/usr/bin/env python3
"""
Barcode Lookup Module for Dram Planner

Provides barcode scanning and product lookup functionality using Open Food Facts API.
Optional dependencies: pyzbar (for scanning), requests (for API calls), pillow (for image processing)
"""

import json
import sys

# Try to import optional dependencies
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from pyzbar import pyzbar
    from PIL import Image
    SCANNING_AVAILABLE = True
except ImportError:
    SCANNING_AVAILABLE = False


OPEN_FOOD_FACTS_API = "https://world.openfoodfacts.org/api/v0/product/{}.json"


def lookup_barcode(barcode):
    """
    Look up product information from Open Food Facts API.
    
    Args:
        barcode (str): Barcode/UPC/EAN code.
        
    Returns:
        dict: Product information if found, None otherwise.
    """
    if not REQUESTS_AVAILABLE:
        print("Error: 'requests' library not installed. Install with: pip install requests")
        return None
    
    if not barcode or not barcode.strip():
        print("Error: Barcode cannot be empty.")
        return None
    
    # Clean barcode (remove spaces, dashes)
    barcode = ''.join(barcode.split())
    barcode = barcode.replace('-', '')
    
    try:
        url = OPEN_FOOD_FACTS_API.format(barcode)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 1 and data.get('product'):
            product = data['product']
            return {
                'name': product.get('product_name', '') or product.get('product_name_en', '') or 'Unknown',
                'brand': product.get('brands', '') or product.get('brand', ''),
                'category': _extract_category(product),
                'abv': _extract_abv(product),
                'volume': _extract_volume(product),
                'description': product.get('generic_name', '') or product.get('generic_name_en', ''),
                'image_url': product.get('image_url', ''),
                'barcode': barcode,
                'source': 'openfoodfacts'
            }
        else:
            print(f"No product found for barcode: {barcode}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Open Food Facts API: {e}")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid response from API.")
        return None
    except Exception as e:
        print(f"Error looking up barcode: {e}")
        return None


def _extract_category(product):
    """Extract category from product data, mapping to spirits categories."""
    # Try various category fields
    categories = product.get('categories', '')
    categories_tags = product.get('categories_tags', [])
    
    # Map Open Food Facts categories to our categories
    category_map = {
        'whisky': 'scotch',
        'whiskey': 'bourbon',
        'bourbon': 'bourbon',
        'scotch': 'scotch',
        'irish whiskey': 'irish',
        'irish': 'irish',
        'gin': 'clear',
        'vodka': 'clear',
        'rum': 'clear',
        'tequila': 'clear',
        'liqueur': 'liqueur',
        'cognac': 'clear',
        'brandy': 'clear'
    }
    
    # Check categories_tags first (more specific)
    for tag in categories_tags:
        tag_lower = tag.lower()
        for key, value in category_map.items():
            if key in tag_lower:
                return value
    
    # Check categories string
    categories_lower = categories.lower()
    for key, value in category_map.items():
        if key in categories_lower:
            return value
    
    # Default to 'other' if no match
    return 'other'


def _extract_abv(product):
    """Extract ABV (alcohol by volume) from product data."""
    # Try various ABV fields
    abv_fields = [
        'alcohol_100g',
        'alcohol',
        'alcohol_per_100g',
        'abv',
        'alcohol_by_volume'
    ]
    
    for field in abv_fields:
        value = product.get(field)
        if value:
            try:
                abv = float(value)
                # If it's per 100g, convert to percentage (assuming ~100g = 100ml for spirits)
                if '100g' in field:
                    return abv
                return abv
            except (ValueError, TypeError):
                continue
    
    # Try to extract from product name or description
    name = (product.get('product_name', '') + ' ' + product.get('generic_name', '')).lower()
    import re
    abv_match = re.search(r'(\d+(?:\.\d+)?)\s*%', name)
    if abv_match:
        try:
            return float(abv_match.group(1))
        except (ValueError, TypeError):
            pass
    
    return None


def _extract_volume(product):
    """Extract volume from product data."""
    volume_fields = [
        'quantity',
        'volume',
        'net_quantity',
        'net_weight'
    ]
    
    for field in volume_fields:
        value = product.get(field)
        if value:
            return value
    
    return None


def scan_barcode_from_image(image_path):
    """
    Scan barcode from an image file.
    
    Args:
        image_path (str): Path to image file.
        
    Returns:
        str: Barcode if found, None otherwise.
    """
    if not SCANNING_AVAILABLE:
        print("Error: Barcode scanning not available. Install with: pip install pyzbar pillow")
        print("Note: On macOS, you may also need: brew install zbar")
        return None
    
    try:
        image = Image.open(image_path)
        barcodes = pyzbar.decode(image)
        
        if barcodes:
            # Return first barcode found
            return barcodes[0].data.decode('utf-8')
        else:
            print("No barcode found in image.")
            return None
            
    except FileNotFoundError:
        print(f"Error: Image file not found: {image_path}")
        return None
    except Exception as e:
        print(f"Error scanning barcode: {e}")
        return None


def scan_barcode_from_camera():
    """
    Scan barcode from camera (interactive).
    
    Note: This requires additional setup and may not work on all systems.
    For now, this is a placeholder for future implementation.
    
    Returns:
        str: Barcode if found, None otherwise.
    """
    print("Camera scanning not yet implemented.")
    print("Please use manual UPC entry or scan from image file.")
    return None


def lookup_and_format(barcode):
    """
    Look up barcode and return formatted product information.
    
    Args:
        barcode (str): Barcode/UPC code.
        
    Returns:
        dict: Formatted product information ready for bottle addition.
    """
    product = lookup_barcode(barcode)
    if not product:
        return None
    
    # Format for bottle addition
    formatted = {
        'name': product.get('name', 'Unknown'),
        'category': product.get('category', 'other'),
        'abv': product.get('abv'),
        'barcode': product.get('barcode'),
        'notes': f"Looked up from Open Food Facts. Brand: {product.get('brand', 'N/A')}"
    }
    
    if product.get('description'):
        formatted['notes'] += f". {product.get('description')}"
    
    return formatted

