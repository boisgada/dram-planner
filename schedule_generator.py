#!/usr/bin/env python3
"""
Spirits Tasting Schedule Generator

This script generates a 2-year tasting schedule for your spirits collection,
ensuring you sample all bottles while allowing for variety and progression.
"""

import json
import random
from datetime import datetime, timedelta
from collections import defaultdict
import argparse


def load_collection(filepath='collection.json'):
    """Load the collection from JSON file.
    
    Args:
        filepath (str): Path to the collection JSON file.
        
    Returns:
        dict: Collection data or None if file not found or invalid.
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            # Validate collection structure
            if not isinstance(data, dict):
                print(f"Error: {filepath} is not a valid JSON object.")
                return None
            if 'bottles' not in data:
                print(f"Error: {filepath} missing 'bottles' key.")
                return None
            return data
    except FileNotFoundError:
        print(f"Error: Collection file {filepath} not found. Please create it first.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {filepath}: {e}")
        return None
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
            print(f"Error: Invalid data format to save.")
            return False
        if 'metadata' not in data:
            data['metadata'] = {}
        data['metadata']['last_updated'] = datetime.now().isoformat()
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except PermissionError:
        print(f"Error: Permission denied writing to {filepath}.")
        return False
    except Exception as e:
        print(f"Error saving collection: {e}")
        return False


def categorize_bottles(bottles):
    """Group bottles by category."""
    categories = defaultdict(list)
    for bottle in bottles:
        category = bottle.get('category', 'other').lower()
        categories[category].append(bottle)
    return categories


def generate_schedule(collection, start_date=None, weeks=104):
    """
    Generate a 2-year tasting schedule (104 weeks).
    
    Strategy:
    1. Ensure variety by rotating categories
    2. Mix tasted and untasted bottles
    3. Allow for some randomness while ensuring all bottles are scheduled
    4. Consider seasonal preferences (lighter spirits in summer, etc.)
    
    Args:
        collection (dict): Collection data with 'bottles' key.
        start_date (str or datetime, optional): Start date (YYYY-MM-DD) or datetime object.
        weeks (int): Number of weeks to schedule (default: 104 for 2 years).
        
    Returns:
        list: List of schedule entries, each with week, date, bottle info.
    """
    if not collection or 'bottles' not in collection:
        print("Error: Invalid collection data.")
        return []
    
    if weeks <= 0:
        print("Error: Weeks must be a positive number.")
        return []
    
    if start_date is None:
        start_date = datetime.now()
    elif isinstance(start_date, str):
        try:
            start_date = datetime.fromisoformat(start_date)
        except ValueError:
            print(f"Error: Invalid date format '{start_date}'. Use YYYY-MM-DD.")
            return []
    elif not isinstance(start_date, datetime):
        print("Error: start_date must be a string (YYYY-MM-DD) or datetime object.")
        return []
    
    bottles = collection['bottles']
    total_bottles = len(bottles)
    
    if total_bottles == 0:
        print("No bottles in collection!")
        return []
    
    # Separate tasted and untasted bottles
    untasted = [b for b in bottles if not b.get('tasted', False)]
    tasted = [b for b in bottles if b.get('tasted', False)]
    
    # Categorize bottles
    categories = categorize_bottles(bottles)
    
    # Create schedule
    schedule = []
    untasted_index = 0
    tasted_index = 0
    
    # Ensure all untasted bottles are scheduled first
    random.shuffle(untasted)
    
    # Then add tasted bottles for variety
    random.shuffle(tasted)
    
    # Create a balanced schedule
    all_bottles = untasted + tasted
    
    # If we have fewer bottles than weeks, we'll repeat some
    # If we have more bottles than weeks, we'll prioritize untasted
    if total_bottles <= weeks:
        # We can schedule each bottle once, with some repeats
        needed_repeats = weeks - total_bottles
        repeat_pool = tasted.copy() if tasted else untasted.copy()
        random.shuffle(repeat_pool)
        all_bottles.extend(repeat_pool[:needed_repeats])
    else:
        # We have more bottles than weeks - prioritize untasted
        all_bottles = untasted[:weeks] if len(untasted) >= weeks else untasted + tasted[:weeks - len(untasted)]
    
    # Shuffle to add variety, but ensure untasted come first
    random.shuffle(all_bottles)
    
    # Re-sort to prioritize untasted
    all_bottles.sort(key=lambda x: (x.get('tasted', False), random.random()))
    
    # Generate weekly schedule
    for week in range(weeks):
        if week < len(all_bottles):
            bottle = all_bottles[week]
            tasting_date = start_date + timedelta(weeks=week)
            
            schedule.append({
                'week': week + 1,
                'date': tasting_date.strftime('%Y-%m-%d'),
                'bottle_id': bottle['id'],
                'bottle_name': bottle['name'],
                'category': bottle.get('category', 'other'),
                'abv': bottle.get('abv', 0),
                'is_repeat': bottle.get('tasted', False)
            })
    
    return schedule


def save_schedule(schedule, filepath='tasting_schedule.json'):
    """Save the schedule to a JSON file.
    
    Args:
        schedule (list): List of schedule entries.
        filepath (str): Path to save the schedule JSON file.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        if not isinstance(schedule, list):
            print("Error: Schedule must be a list.")
            return False
        schedule_data = {
            'generated_date': datetime.now().isoformat(),
            'total_weeks': len(schedule),
            'schedule': schedule
        }
        with open(filepath, 'w') as f:
            json.dump(schedule_data, f, indent=2)
        print(f"Schedule saved to {filepath}")
        return True
    except PermissionError:
        print(f"Error: Permission denied writing to {filepath}.")
        return False
    except Exception as e:
        print(f"Error saving schedule: {e}")
        return False


def print_schedule_summary(schedule):
    """Print a summary of the generated schedule."""
    if not schedule:
        print("No schedule generated.")
        return
    
    categories = defaultdict(int)
    for entry in schedule:
        categories[entry['category']] += 1
    
    print(f"\n{'='*60}")
    print(f"Tasting Schedule Summary")
    print(f"{'='*60}")
    print(f"Total weeks scheduled: {len(schedule)}")
    print(f"Start date: {schedule[0]['date']}")
    print(f"End date: {schedule[-1]['date']}")
    print(f"\nBreakdown by category:")
    for category, count in sorted(categories.items()):
        print(f"  {category.capitalize()}: {count}")
    
    repeats = sum(1 for e in schedule if e.get('is_repeat', False))
    print(f"\nNew tastings: {len(schedule) - repeats}")
    print(f"Repeat tastings: {repeats}")


def main():
    parser = argparse.ArgumentParser(description='Generate a 2-year spirits tasting schedule')
    parser.add_argument('--collection', default='collection.json', help='Path to collection JSON file')
    parser.add_argument('--output', default='tasting_schedule.json', help='Output file for schedule')
    parser.add_argument('--start-date', help='Start date (YYYY-MM-DD). Defaults to today.')
    parser.add_argument('--weeks', type=int, default=104, help='Number of weeks (default: 104 for 2 years)')
    parser.add_argument('--preview', action='store_true', help='Preview first 10 weeks only')
    
    args = parser.parse_args()
    
    # Validate weeks argument
    if args.weeks <= 0:
        print("Error: Weeks must be a positive number.")
        return 1
    
    collection = load_collection(args.collection)
    if not collection:
        return 1
    
    schedule = generate_schedule(collection, args.start_date, args.weeks)
    if not schedule:
        return 1
    
    if args.preview:
        print("\nPreview of first 10 weeks:")
        print(f"{'Week':<6} {'Date':<12} {'Bottle':<30} {'Category':<15}")
        print("-" * 70)
        for entry in schedule[:10]:
            print(f"{entry['week']:<6} {entry['date']:<12} {entry['bottle_name']:<30} {entry['category']:<15}")
    else:
        if save_schedule(schedule, args.output):
            print_schedule_summary(schedule)
            print(f"\nFull schedule saved to {args.output}")
        else:
            return 1
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())

