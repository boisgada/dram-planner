#!/usr/bin/env python3
"""
Helper script to add bottles to your collection.
Supports manual entry, CSV import, and barcode lookup.
"""

import json
import argparse
from datetime import datetime
import barcode_lookup
import import_manager


def load_collection(filepath='collection.json'):
    """Load the collection from JSON file.
    
    Args:
        filepath (str): Path to the collection JSON file.
        
    Returns:
        dict: Collection data, or new empty collection if file not found.
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            # Validate structure
            if not isinstance(data, dict):
                print(f"Error: {filepath} is not a valid JSON object. Creating new collection.")
                return {'bottles': [], 'metadata': {'total_bottles': 0, 'last_updated': ''}}
            if 'bottles' not in data:
                data['bottles'] = []
            if 'metadata' not in data:
                data['metadata'] = {'total_bottles': 0, 'last_updated': ''}
            return data
    except FileNotFoundError:
        return {'bottles': [], 'metadata': {'total_bottles': 0, 'last_updated': ''}}
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {filepath}: {e}. Creating new collection.")
        return {'bottles': [], 'metadata': {'total_bottles': 0, 'last_updated': ''}}
    except PermissionError:
        print(f"Error: Permission denied reading {filepath}.")
        return None
    except Exception as e:
        print(f"Error loading collection: {e}")
        return None


def save_collection(data, filepath='collection.json'):
    """Save the collection to JSON file.
    
    Args:
        data (dict): Collection data to save.
        filepath (str): Path to save the collection JSON file.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        if not isinstance(data, dict):
            print("Error: Invalid data format to save.")
            return False
        if 'metadata' not in data:
            data['metadata'] = {}
        data['metadata']['last_updated'] = datetime.now().isoformat()
        data['metadata']['total_bottles'] = len(data.get('bottles', []))
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except PermissionError:
        print(f"Error: Permission denied writing to {filepath}.")
        return False
    except Exception as e:
        print(f"Error saving collection: {e}")
        return False


def add_bottle(name, category, abv=None, price_paid=None, purchase_date=None, notes=None, barcode=None, filepath='collection.json'):
    """Add a new bottle to the collection.
    
    Args:
        name (str): Bottle name (required).
        category (str): Category (bourbon, scotch, irish, clear, liqueur, etc.).
        abv (float, optional): Alcohol by volume (%).
        price_paid (float, optional): Purchase price.
        purchase_date (str, optional): Purchase date (YYYY-MM-DD).
        notes (str, optional): Additional notes.
        barcode (str, optional): Barcode/UPC code.
        filepath (str): Path to collection file.
        
    Returns:
        int: Bottle ID if successful, None otherwise.
    """
    # Validate inputs
    if not name or not name.strip():
        print("Error: Bottle name is required.")
        return None
    
    if not category or not category.strip():
        print("Error: Category is required.")
        return None
    
    # Validate ABV if provided
    if abv is not None:
        try:
            abv = float(abv)
            if abv < 0 or abv > 100:
                print(f"Warning: ABV {abv}% seems unusual. Continuing anyway.")
        except (ValueError, TypeError):
            print(f"Error: Invalid ABV value: {abv}")
            return None
    
    # Validate price if provided
    if price_paid is not None:
        try:
            price_paid = float(price_paid)
            if price_paid < 0:
                print(f"Error: Price cannot be negative.")
                return None
        except (ValueError, TypeError):
            print(f"Error: Invalid price value: {price_paid}")
            return None
    
    # Validate date format if provided
    if purchase_date:
        try:
            datetime.strptime(purchase_date, '%Y-%m-%d')
        except ValueError:
            print(f"Error: Invalid date format '{purchase_date}'. Use YYYY-MM-DD.")
            return None
    
    collection = load_collection(filepath)
    if collection is None:
        return None
    
    # Find next available ID
    if collection.get('bottles'):
        try:
            next_id = max(b.get('id', 0) for b in collection['bottles']) + 1
        except (ValueError, TypeError):
            next_id = 1
    else:
        next_id = 1
    
    bottle = {
        'id': next_id,
        'name': name,
        'category': category.lower(),
        'abv': abv if abv else 0.0,
        'price_paid': price_paid if price_paid else 0.0,
        'purchase_date': purchase_date if purchase_date else '',
        'opened_date': '',
        'notes': notes if notes else '',
        'barcode': barcode if barcode else '',
        'tasted': False,
        'tasting_date': None,
        'rating': None,
        'tasting_notes': ''
    }
    
    collection['bottles'].append(bottle)
    if save_collection(collection, filepath):
        print(f"✓ Added bottle: {name} (ID: {next_id})")
        return next_id
    else:
        print("Error: Failed to save collection.")
        return None


def add_bottles_from_import(bottles_data, filepath='collection.json'):
    """Add multiple bottles from imported data.
    
    Args:
        bottles_data (list): List of normalized bottle dictionaries.
        filepath (str): Path to collection file.
        
    Returns:
        int: Number of bottles added, or None on error.
    """
    collection = load_collection(filepath)
    if collection is None:
        return None
    
    if collection['bottles']:
        next_id = max(b['id'] for b in collection['bottles']) + 1
    else:
        next_id = 1
    
    added = 0
    for bottle_data in bottles_data:
        bottle = {
            'id': next_id,
            'name': bottle_data['name'],
            'category': bottle_data['category'],
            'abv': bottle_data['abv'],
            'price_paid': bottle_data['price_paid'],
            'purchase_date': bottle_data['purchase_date'],
            'opened_date': bottle_data['opened_date'],
            'notes': bottle_data['notes'],
            'barcode': bottle_data['barcode'],
            'tasted': bottle_data['tasted'],
            'tasting_date': bottle_data['tasting_date'],
            'rating': bottle_data['rating'],
            'tasting_notes': bottle_data['tasting_notes']
        }
        
        collection['bottles'].append(bottle)
        next_id += 1
        added += 1
    
    if save_collection(collection, filepath):
        print(f"✓ Added {added} bottles to collection")
        return added
    else:
        print("Error: Failed to save collection.")
        return None


def add_bottles_from_csv(csv_file, filepath='collection.json', preview=False):
    """Add multiple bottles from a CSV file (enhanced).
    
    Args:
        csv_file (str): Path to CSV file.
        filepath (str): Path to collection file.
        preview (bool): If True, only preview without adding.
        
    Returns:
        int: Number of bottles added, or None on error.
    """
    bottles, errors, warnings = import_manager.import_from_csv(csv_file, preview=preview)
    
    if preview:
        import_manager.print_import_preview(bottles, errors, warnings)
        return len(bottles) if not errors else None
    
    if errors:
        print(f"\nErrors found in CSV file:")
        for error in errors[:10]:
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")
        response = input("\nContinue importing valid bottles? (yes/no): ")
        if response.lower() not in ('yes', 'y'):
            print("Import cancelled.")
            return None
    
    if warnings:
        for warning in warnings:
            print(f"Warning: {warning}")
    
    if not bottles:
        print("No valid bottles to import.")
        return None
    
    return add_bottles_from_import(bottles, filepath)


def add_bottles_from_json(json_file, filepath='collection.json', preview=False):
    """Add multiple bottles from a JSON file.
    
    Args:
        json_file (str): Path to JSON file.
        filepath (str): Path to collection file.
        preview (bool): If True, only preview without adding.
        
    Returns:
        int: Number of bottles added, or None on error.
    """
    bottles, errors, warnings = import_manager.import_from_json(json_file, preview=preview)
    
    if preview:
        import_manager.print_import_preview(bottles, errors, warnings)
        return len(bottles) if not errors else None
    
    if errors:
        print(f"\nErrors found in JSON file:")
        for error in errors[:10]:
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")
        response = input("\nContinue importing valid bottles? (yes/no): ")
        if response.lower() not in ('yes', 'y'):
            print("Import cancelled.")
            return None
    
    if warnings:
        for warning in warnings:
            print(f"Warning: {warning}")
    
    if not bottles:
        print("No valid bottles to import.")
        return None
    
    return add_bottles_from_import(bottles, filepath)


def add_bottles_from_excel(excel_file, sheet_name=None, filepath='collection.json', preview=False):
    """Add multiple bottles from an Excel file.
    
    Args:
        excel_file (str): Path to Excel file (.xlsx).
        sheet_name (str, optional): Sheet name. Uses first sheet if not specified.
        filepath (str): Path to collection file.
        preview (bool): If True, only preview without adding.
        
    Returns:
        int: Number of bottles added, or None on error.
    """
    bottles, errors, warnings = import_manager.import_from_excel(excel_file, sheet_name, preview=preview)
    
    if preview:
        import_manager.print_import_preview(bottles, errors, warnings)
        return len(bottles) if not errors else None
    
    if errors:
        print(f"\nErrors found in Excel file:")
        for error in errors[:10]:
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")
        response = input("\nContinue importing valid bottles? (yes/no): ")
        if response.lower() not in ('yes', 'y'):
            print("Import cancelled.")
            return None
    
    if warnings:
        for warning in warnings:
            print(f"Warning: {warning}")
    
    if not bottles:
        print("No valid bottles to import.")
        return None
    
    return add_bottles_from_import(bottles, filepath)


def add_bottle_from_barcode(barcode, price_paid=None, purchase_date=None, notes=None, filepath='collection.json'):
    """Add a bottle by looking up its barcode.
    
    Args:
        barcode (str): Barcode/UPC code or path to image file.
        price_paid (float, optional): Purchase price.
        purchase_date (str, optional): Purchase date (YYYY-MM-DD).
        notes (str, optional): Additional notes.
        filepath (str): Path to collection file.
        
    Returns:
        int: Bottle ID if successful, None otherwise.
    """
    # Check if barcode is an image file path
    import os
    if os.path.exists(barcode):
        # Try to scan barcode from image
        scanned_barcode = barcode_lookup.scan_barcode_from_image(barcode)
        if scanned_barcode:
            barcode = scanned_barcode
            print(f"Scanned barcode: {barcode}")
        else:
            print("Error: Could not scan barcode from image.")
            return None
    
    # Look up product information
    print(f"Looking up barcode: {barcode}...")
    product = barcode_lookup.lookup_and_format(barcode)
    
    if not product:
        print("Error: Could not find product information. Please add manually.")
        return None
    
    # Merge additional information
    additional_notes = notes if notes else ''
    if product.get('notes'):
        if additional_notes:
            additional_notes = f"{additional_notes}. {product.get('notes')}"
        else:
            additional_notes = product.get('notes')
    
    # Add bottle with looked-up information
    return add_bottle(
        name=product.get('name', 'Unknown'),
        category=product.get('category', 'other'),
        abv=product.get('abv'),
        price_paid=price_paid,
        purchase_date=purchase_date,
        notes=additional_notes,
        barcode=barcode,
        filepath=filepath
    )


def main():
    parser = argparse.ArgumentParser(description='Add bottles to your collection')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Add single bottle
    add_parser = subparsers.add_parser('add', help='Add a single bottle manually')
    add_parser.add_argument('name', help='Bottle name')
    add_parser.add_argument('category', help='Category (bourbon, scotch, irish, clear, liqueur, etc.)')
    add_parser.add_argument('--abv', type=float, help='Alcohol by volume (%)')
    add_parser.add_argument('--price', type=float, help='Price paid')
    add_parser.add_argument('--purchase-date', help='Purchase date (YYYY-MM-DD)')
    add_parser.add_argument('--notes', help='Additional notes')
    add_parser.add_argument('--barcode', help='Barcode/UPC code')
    
    # Add from barcode
    barcode_parser = subparsers.add_parser('barcode', help='Add bottle by barcode lookup')
    barcode_parser.add_argument('barcode', help='Barcode/UPC code or path to image file')
    barcode_parser.add_argument('--price', type=float, help='Price paid')
    barcode_parser.add_argument('--purchase-date', help='Purchase date (YYYY-MM-DD)')
    barcode_parser.add_argument('--notes', help='Additional notes')
    
    # Add from CSV (enhanced)
    csv_parser = subparsers.add_parser('csv', help='Add bottles from CSV file')
    csv_parser.add_argument('csv_file', help='Path to CSV file')
    csv_parser.add_argument('--preview', action='store_true', help='Preview import without adding')
    
    # Add from JSON
    json_parser = subparsers.add_parser('json', help='Add bottles from JSON file')
    json_parser.add_argument('json_file', help='Path to JSON file')
    json_parser.add_argument('--preview', action='store_true', help='Preview import without adding')
    
    # Add from Excel
    excel_parser = subparsers.add_parser('excel', help='Add bottles from Excel file (.xlsx)')
    excel_parser.add_argument('excel_file', help='Path to Excel file')
    excel_parser.add_argument('--sheet', help='Sheet name (uses first sheet if not specified)')
    excel_parser.add_argument('--preview', action='store_true', help='Preview import without adding')
    
    args = parser.parse_args()
    
    if args.command == 'add':
        add_bottle(args.name, args.category, args.abv, args.price, 
                  args.purchase_date, args.notes, args.barcode)
    elif args.command == 'barcode':
        add_bottle_from_barcode(args.barcode, args.price, args.purchase_date, args.notes)
    elif args.command == 'csv':
        add_bottles_from_csv(args.csv_file, preview=args.preview)
    elif args.command == 'json':
        add_bottles_from_json(args.json_file, preview=args.preview)
    elif args.command == 'excel':
        add_bottles_from_excel(args.excel_file, args.sheet, preview=args.preview)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

