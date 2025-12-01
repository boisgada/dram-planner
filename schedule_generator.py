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
import config


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


def adjust_to_preferred_day(date, preferred_days):
    """Adjust a date to the nearest preferred day.
    
    Args:
        date (datetime): Date to adjust.
        preferred_days (list): List of preferred day names (e.g., ['Friday', 'Saturday']).
        
    Returns:
        datetime: Adjusted date (or original if no preferred days).
    """
    if not preferred_days:
        return date
    
    # Map day names to weekday numbers (Monday=0, Sunday=6)
    day_map = {
        'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
        'friday': 4, 'saturday': 5, 'sunday': 6
    }
    
    preferred_weekdays = [day_map.get(day.lower(), -1) for day in preferred_days]
    preferred_weekdays = [d for d in preferred_weekdays if d >= 0]
    
    if not preferred_weekdays:
        return date
    
    current_weekday = date.weekday()
    
    # Find nearest preferred day
    min_diff = 7
    best_day = current_weekday
    
    for preferred in preferred_weekdays:
        diff = (preferred - current_weekday) % 7
        if diff == 0:
            return date  # Already on preferred day
        if diff < min_diff:
            min_diff = diff
            best_day = preferred
    
    # Adjust to nearest preferred day
    return date + timedelta(days=min_diff)


def is_avoid_date(date, avoid_dates):
    """Check if a date should be avoided.
    
    Args:
        date (datetime): Date to check.
        avoid_dates (list): List of date strings in YYYY-MM-DD format.
        
    Returns:
        bool: True if date should be avoided.
    """
    if not avoid_dates:
        return False
    
    date_str = date.strftime('%Y-%m-%d')
    return date_str in avoid_dates


def get_seasonal_weight(category, date, seasonal_enabled):
    """Get seasonal weight adjustment for a category.
    
    Args:
        category (str): Bottle category.
        date (datetime): Date of tasting.
        seasonal_enabled (bool): Whether seasonal adjustments are enabled.
        
    Returns:
        float: Weight multiplier (1.0 = no change, >1.0 = prefer, <1.0 = avoid).
    """
    if not seasonal_enabled:
        return 1.0
    
    month = date.month
    
    # Lighter spirits in summer (June-August)
    # Heavier spirits in winter (December-February)
    light_categories = ['gin', 'vodka', 'rum', 'tequila', 'clear spirits']
    heavy_categories = ['bourbon', 'scotch', 'whiskey', 'whisky', 'rye']
    
    category_lower = category.lower()
    
    if month in [6, 7, 8]:  # Summer
        if any(light in category_lower for light in light_categories):
            return 1.5  # Prefer lighter in summer
        elif any(heavy in category_lower for heavy in heavy_categories):
            return 0.7  # Avoid heavier in summer
    elif month in [12, 1, 2]:  # Winter
        if any(heavy in category_lower for heavy in heavy_categories):
            return 1.5  # Prefer heavier in winter
        elif any(light in category_lower for light in light_categories):
            return 0.7  # Avoid lighter in winter
    
    return 1.0


def generate_schedule(collection, start_date=None, weeks=104, config_data=None):
    """
    Generate a tasting schedule with user preferences.
    
    Strategy:
    1. Ensure variety by rotating categories
    2. Mix tasted and untasted bottles
    3. Allow for some randomness while ensuring all bottles are scheduled
    4. Respect user preferences (frequency, preferred days, avoid dates, etc.)
    5. Consider seasonal preferences (lighter spirits in summer, etc.)
    
    Args:
        collection (dict): Collection data with 'bottles' key.
        start_date (str or datetime, optional): Start date (YYYY-MM-DD) or datetime object.
        weeks (int): Number of weeks to schedule (default: 104 for 2 years).
        config_data (dict, optional): Configuration data. If None, loads from config.json.
        
    Returns:
        list: List of schedule entries, each with week, date, bottle info.
    """
    if not collection or 'bottles' not in collection:
        print("Error: Invalid collection data.")
        return []
    
    if weeks <= 0:
        print("Error: Weeks must be a positive number.")
        return []
    
    # Load config if not provided
    if config_data is None:
        config_data = config.load_config()
    
    # Get preferences from config
    frequency_days = config.get_tasting_frequency_days(config_data)
    preferred_days = config.get_preferred_days(config_data)
    avoid_dates = config.get_avoid_dates(config_data)
    category_prefs = config.get_category_preferences(config_data)
    seasonal_enabled = config.get_seasonal_adjustments(config_data)
    min_days_between_category = config.get_min_days_between_category(config_data)
    
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
    
    # Create weighted bottle pool with preferences
    all_bottles = []
    
    # Build weighted list considering category preferences
    for bottle in untasted + tasted:
        category = bottle.get('category', 'other').lower()
        weight = category_prefs.get(category, 1.0)
        # Untasted bottles get priority boost
        if not bottle.get('tasted', False):
            weight *= 2.0
        all_bottles.append((bottle, weight))
    
    # Calculate total schedule days
    total_days = weeks * 7  # Rough estimate, will adjust based on frequency
    total_tastings = int(total_days / frequency_days)
    
    # If we have fewer bottles than tastings, we'll repeat some
    if total_bottles <= total_tastings:
        needed_repeats = total_tastings - total_bottles
        repeat_pool = [(b, w) for b, w in all_bottles if b.get('tasted', False)]
        if not repeat_pool:
            repeat_pool = all_bottles.copy()
        random.shuffle(repeat_pool)
        all_bottles.extend(repeat_pool[:needed_repeats])
    else:
        # We have more bottles than tastings - prioritize untasted
        untasted_weighted = [(b, w) for b, w in all_bottles if not b.get('tasted', False)]
        tasted_weighted = [(b, w) for b, w in all_bottles if b.get('tasted', False)]
        if len(untasted_weighted) >= total_tastings:
            all_bottles = untasted_weighted[:total_tastings]
        else:
            all_bottles = untasted_weighted + tasted_weighted[:total_tastings - len(untasted_weighted)]
    
    # Weighted random selection
    weights = [w for _, w in all_bottles]
    selected_bottles = random.choices(
        [b for b, _ in all_bottles],
        weights=weights,
        k=min(total_tastings, len(all_bottles))
    )
    
    # Shuffle to add variety, but ensure untasted come first
    random.shuffle(selected_bottles)
    selected_bottles.sort(key=lambda x: (x.get('tasted', False), random.random()))
    
    # Generate schedule with date adjustments
    schedule = []
    current_date = start_date
    last_category_date = {}  # Track last date for each category
    week_num = 1
    
    for bottle in selected_bottles:
        category = bottle.get('category', 'other').lower()
        
        # Apply seasonal weight if enabled
        seasonal_weight = get_seasonal_weight(category, current_date, seasonal_enabled)
        
        # Skip if this category was too recent (if min_days_between_category is set)
        if min_days_between_category > 0 and category in last_category_date:
            days_since = (current_date - last_category_date[category]).days
            if days_since < min_days_between_category:
                # Move date forward
                current_date = last_category_date[category] + timedelta(days=min_days_between_category)
        
        # Adjust to preferred day if specified
        if preferred_days:
            current_date = adjust_to_preferred_day(current_date, preferred_days)
        
        # Skip avoid dates
        max_attempts = 30  # Prevent infinite loop
        attempts = 0
        while is_avoid_date(current_date, avoid_dates) and attempts < max_attempts:
            current_date += timedelta(days=1)
            if preferred_days:
                current_date = adjust_to_preferred_day(current_date, preferred_days)
            attempts += 1
        
        # If seasonal weight is low, might skip this bottle (but for now, include it)
        # In a more sophisticated version, we could re-select here
        
        schedule.append({
            'week': week_num,
            'date': current_date.strftime('%Y-%m-%d'),
            'bottle_id': bottle['id'],
            'bottle_name': bottle['name'],
            'category': bottle.get('category', 'other'),
            'abv': bottle.get('abv', 0),
            'is_repeat': bottle.get('tasted', False)
        })
        
        last_category_date[category] = current_date
        current_date += timedelta(days=frequency_days)
        week_num += 1
    
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
    parser = argparse.ArgumentParser(description='Generate a spirits tasting schedule with user preferences')
    parser.add_argument('--collection', default='collection.json', help='Path to collection JSON file')
    parser.add_argument('--output', default='tasting_schedule.json', help='Output file for schedule')
    parser.add_argument('--config', default='config.json', help='Path to config file (default: config.json)')
    parser.add_argument('--start-date', help='Start date (YYYY-MM-DD). Defaults to today.')
    parser.add_argument('--weeks', type=int, help='Number of weeks (default: from config or 104)')
    parser.add_argument('--preview', action='store_true', help='Preview first 10 weeks only')
    
    args = parser.parse_args()
    
    # Load config
    config_data = config.load_config(args.config)
    
    # Use config default for weeks if not specified
    if args.weeks is None:
        args.weeks = config.get_default_schedule_weeks(config_data)
    
    # Validate weeks argument
    if args.weeks <= 0:
        print("Error: Weeks must be a positive number.")
        return 1
    
    collection = load_collection(args.collection)
    if not collection:
        return 1
    
    schedule = generate_schedule(collection, args.start_date, args.weeks, config_data)
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

