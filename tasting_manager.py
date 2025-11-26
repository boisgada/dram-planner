#!/usr/bin/env python3
"""
Spirits Tasting Manager

CLI tool for managing your tasting schedule, recording notes, and tracking progress.
"""

import json
import argparse
from datetime import datetime
from collections import defaultdict


def load_json(filepath):
    """Load JSON file.
    
    Args:
        filepath (str): Path to JSON file.
        
    Returns:
        dict: JSON data or None if file not found or invalid.
    """
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {filepath}: {e}")
        return None
    except PermissionError:
        print(f"Error: Permission denied reading {filepath}.")
        return None
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None


def save_json(data, filepath):
    """Save data to JSON file.
    
    Args:
        data (dict): Data to save.
        filepath (str): Path to save JSON file.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except PermissionError:
        print(f"Error: Permission denied writing to {filepath}.")
        return False
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False


def record_tasting(collection_file, bottle_id, rating, notes, date=None):
    """Record a tasting for a specific bottle.
    
    Args:
        collection_file (str): Path to collection JSON file.
        bottle_id (int): ID of the bottle to record.
        rating (float): Rating (0-10).
        notes (str): Tasting notes.
        date (str, optional): Date in YYYY-MM-DD format. Defaults to today.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    # Validate inputs
    if not isinstance(bottle_id, int) or bottle_id < 1:
        print(f"Error: Invalid bottle ID: {bottle_id}")
        return False
    
    if not isinstance(rating, (int, float)) or rating < 0 or rating > 10:
        print(f"Error: Rating must be between 0 and 10. Got: {rating}")
        return False
    
    collection = load_json(collection_file)
    if not collection:
        print(f"Error: Collection file {collection_file} not found or invalid!")
        return False
    
    if 'bottles' not in collection:
        print(f"Error: Invalid collection structure in {collection_file}.")
        return False
    
    bottle = None
    for b in collection['bottles']:
        if b.get('id') == bottle_id:
            bottle = b
            break
    
    if not bottle:
        print(f"Error: Bottle with ID {bottle_id} not found!")
        return False
    
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    else:
        # Validate date format
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            print(f"Error: Invalid date format '{date}'. Use YYYY-MM-DD.")
            return False
    
    bottle['tasted'] = True
    bottle['tasting_date'] = date
    bottle['rating'] = float(rating)
    bottle['tasting_notes'] = str(notes)
    
    if not bottle.get('opened_date'):
        bottle['opened_date'] = date
    
    if save_json(collection, collection_file):
        print(f"✓ Recorded tasting for {bottle['name']} on {date}")
        print(f"  Rating: {rating}/10")
        print(f"  Notes: {notes[:50]}..." if len(notes) > 50 else f"  Notes: {notes}")
        return True
    return False


def view_schedule(schedule_file, weeks=10):
    """View upcoming tasting schedule.
    
    Args:
        schedule_file (str): Path to schedule JSON file.
        weeks (int): Number of weeks to show (default: 10).
    """
    if weeks <= 0:
        print("Error: Weeks must be a positive number.")
        return
    
    schedule_data = load_json(schedule_file)
    if not schedule_data:
        print(f"Error: Schedule file {schedule_file} not found or invalid!")
        return
    
    if 'schedule' not in schedule_data:
        print(f"Error: Invalid schedule structure in {schedule_file}.")
        return
    
    schedule = schedule_data['schedule']
    today = datetime.now().date()
    
    print(f"\n{'='*80}")
    print(f"Upcoming Tastings (next {weeks} weeks)")
    print(f"{'='*80}")
    print(f"{'Week':<6} {'Date':<12} {'Bottle':<35} {'Category':<15} {'ABV':<6}")
    print("-" * 80)
    
    shown = 0
    for entry in schedule:
        try:
            entry_date = datetime.strptime(entry['date'], '%Y-%m-%d').date()
            if entry_date >= today and shown < weeks:
                print(f"{entry.get('week', 'N/A'):<6} {entry['date']:<12} {entry.get('bottle_name', 'Unknown'):<35} "
                      f"{entry.get('category', 'other'):<15} {entry.get('abv', 0):<6}")
                shown += 1
        except (KeyError, ValueError) as e:
            print(f"Warning: Skipping invalid schedule entry: {e}")
            continue
    
    if shown == 0:
        print("No upcoming tastings found.")


def view_progress(collection_file):
    """View tasting progress statistics.
    
    Args:
        collection_file (str): Path to collection JSON file.
    """
    collection = load_json(collection_file)
    if not collection:
        print(f"Error: Collection file {collection_file} not found or invalid!")
        return
    
    if 'bottles' not in collection:
        print(f"Error: Invalid collection structure in {collection_file}.")
        return
    
    bottles = collection['bottles']
    total = len(bottles)
    
    if total == 0:
        print("No bottles in collection.")
        return
    
    tasted = sum(1 for b in bottles if b.get('tasted', False))
    untasted = total - tasted
    
    categories = defaultdict(lambda: {'total': 0, 'tasted': 0})
    ratings = []
    
    for bottle in bottles:
        cat = bottle.get('category', 'other')
        categories[cat]['total'] += 1
        if bottle.get('tasted', False):
            categories[cat]['tasted'] += 1
            rating = bottle.get('rating')
            if rating is not None:
                try:
                    ratings.append(float(rating))
                except (ValueError, TypeError):
                    pass
    
    print(f"\n{'='*60}")
    print(f"Tasting Progress")
    print(f"{'='*60}")
    print(f"Total bottles: {total}")
    if total > 0:
        print(f"Tasted: {tasted} ({tasted/total*100:.1f}%)")
        print(f"Untasted: {untasted} ({untasted/total*100:.1f}%)")
    
    if ratings:
        avg_rating = sum(ratings) / len(ratings)
        print(f"\nAverage rating: {avg_rating:.1f}/10")
        print(f"Highest rated: {max(ratings)}/10")
        print(f"Lowest rated: {min(ratings)}/10")
    
    print(f"\nProgress by category:")
    for cat in sorted(categories.keys()):
        stats = categories[cat]
        pct = (stats['tasted'] / stats['total'] * 100) if stats['total'] > 0 else 0
        print(f"  {cat.capitalize():<15} {stats['tasted']}/{stats['total']} ({pct:.1f}%)")


def list_bottles(collection_file, category=None, tasted=None):
    """List bottles in collection with optional filters."""
    collection = load_json(collection_file)
    if not collection:
        print(f"Collection file {collection_file} not found!")
        return
    
    bottles = collection['bottles']
    
    if category:
        bottles = [b for b in bottles if b.get('category', '').lower() == category.lower()]
    
    if tasted is not None:
        bottles = [b for b in bottles if b.get('tasted', False) == tasted]
    
    print(f"\n{'='*80}")
    print(f"Bottles in Collection" + (f" ({category})" if category else ""))
    print(f"{'='*80}")
    print(f"{'ID':<6} {'Name':<35} {'Category':<15} {'Tasted':<8} {'Rating':<8}")
    print("-" * 80)
    
    for bottle in sorted(bottles, key=lambda x: x['name']):
        tasted_str = "✓" if bottle.get('tasted', False) else "✗"
        rating = str(bottle.get('rating', 'N/A')) if bottle.get('rating') else 'N/A'
        print(f"{bottle['id']:<6} {bottle['name']:<35} {bottle.get('category', 'other'):<15} "
              f"{tasted_str:<8} {rating:<8}")


def find_bottle(collection_file, search_term):
    """Find a bottle by name or ID."""
    collection = load_json(collection_file)
    if not collection:
        print(f"Collection file {collection_file} not found!")
        return
    
    bottles = collection['bottles']
    results = []
    
    try:
        bottle_id = int(search_term)
        results = [b for b in bottles if b['id'] == bottle_id]
    except ValueError:
        search_lower = search_term.lower()
        results = [b for b in bottles if search_lower in b['name'].lower()]
    
    if not results:
        print(f"No bottles found matching '{search_term}'")
        return
    
    for bottle in results:
        print(f"\n{'='*60}")
        print(f"Bottle Details")
        print(f"{'='*60}")
        print(f"ID: {bottle['id']}")
        print(f"Name: {bottle['name']}")
        print(f"Category: {bottle.get('category', 'other')}")
        print(f"ABV: {bottle.get('abv', 'N/A')}%")
        print(f"Tasted: {'Yes' if bottle.get('tasted', False) else 'No'}")
        if bottle.get('tasted', False):
            print(f"Tasting Date: {bottle.get('tasting_date', 'N/A')}")
            print(f"Rating: {bottle.get('rating', 'N/A')}/10")
            print(f"Notes: {bottle.get('tasting_notes', 'N/A')}")


def main():
    parser = argparse.ArgumentParser(description='Manage your spirits tasting schedule and notes')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Record tasting
    record_parser = subparsers.add_parser('record', help='Record a tasting')
    record_parser.add_argument('--collection', default='collection.json')
    record_parser.add_argument('bottle_id', type=int, help='Bottle ID')
    record_parser.add_argument('rating', type=float, help='Rating (0-10)')
    record_parser.add_argument('notes', help='Tasting notes')
    record_parser.add_argument('--date', help='Date (YYYY-MM-DD), defaults to today')
    
    # View schedule
    schedule_parser = subparsers.add_parser('schedule', help='View tasting schedule')
    schedule_parser.add_argument('--schedule', default='tasting_schedule.json')
    schedule_parser.add_argument('--weeks', type=int, default=10, help='Number of weeks to show')
    
    # View progress
    progress_parser = subparsers.add_parser('progress', help='View tasting progress')
    progress_parser.add_argument('--collection', default='collection.json')
    
    # List bottles
    list_parser = subparsers.add_parser('list', help='List bottles')
    list_parser.add_argument('--collection', default='collection.json')
    list_parser.add_argument('--category', help='Filter by category')
    list_parser.add_argument('--tasted', action='store_true', help='Show only tasted bottles')
    list_parser.add_argument('--untasted', action='store_true', help='Show only untasted bottles')
    
    # Find bottle
    find_parser = subparsers.add_parser('find', help='Find a bottle by name or ID')
    find_parser.add_argument('--collection', default='collection.json')
    find_parser.add_argument('search_term', help='Bottle name or ID')
    
    args = parser.parse_args()
    
    if args.command == 'record':
        record_tasting(args.collection, args.bottle_id, args.rating, args.notes, args.date)
    elif args.command == 'schedule':
        view_schedule(args.schedule, args.weeks)
    elif args.command == 'progress':
        view_progress(args.collection)
    elif args.command == 'list':
        tasted = None
        if args.tasted:
            tasted = True
        elif args.untasted:
            tasted = False
        list_bottles(args.collection, args.category, tasted)
    elif args.command == 'find':
        find_bottle(args.collection, args.search_term)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

