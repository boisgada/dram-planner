#!/usr/bin/env python3
"""
Configuration Management for Dram Planner

Handles user preferences and configuration settings.
"""

import json
import os
from pathlib import Path


DEFAULT_CONFIG = {
    "user_preferences": {
        "tasting_frequency": "weekly",  # weekly, bi-weekly, monthly, custom
        "custom_interval_days": 7,  # For custom frequency
        "preferred_days": [],  # List of day names: ["Friday", "Saturday"]
        "avoid_dates": [],  # List of dates to avoid: ["2024-12-25", "2024-01-01"]
        "category_preferences": {},  # {"bourbon": 2.0, "scotch": 1.5} - weights
        "seasonal_adjustments": False,  # Enable seasonal preferences
        "min_days_between_category": 0,  # Minimum days between same category
        "default_schedule_weeks": 104  # Default schedule duration
    },
    "import_sources": {
        "open_food_facts": {
            "enabled": False,  # Will be True when barcode scanning is implemented
            "api_url": "https://world.openfoodfacts.org/api/v0/product/{}.json"
        }
    },
    "data_files": {
        "collection_file": "collection.json",
        "schedule_file": "tasting_schedule.json"
    }
}


def load_config(filepath='config.json'):
    """Load configuration from JSON file.
    
    Args:
        filepath (str): Path to configuration file.
        
    Returns:
        dict: Configuration data, or default config if file not found.
    """
    if not os.path.exists(filepath):
        # Create default config file
        save_config(DEFAULT_CONFIG, filepath)
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(filepath, 'r') as f:
            config = json.load(f)
            # Merge with defaults to ensure all keys exist
            merged = DEFAULT_CONFIG.copy()
            merged.update(config)
            # Deep merge for nested dictionaries
            if 'user_preferences' in config:
                merged['user_preferences'].update(config['user_preferences'])
            if 'import_sources' in config:
                merged['import_sources'].update(config['import_sources'])
            if 'data_files' in config:
                merged['data_files'].update(config['data_files'])
            return merged
    except (json.JSONDecodeError, PermissionError) as e:
        print(f"Error loading config: {e}. Using defaults.")
        return DEFAULT_CONFIG.copy()


def save_config(config, filepath='config.json'):
    """Save configuration to JSON file.
    
    Args:
        config (dict): Configuration data to save.
        filepath (str): Path to save configuration file.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except PermissionError:
        print(f"Error: Permission denied writing to {filepath}.")
        return False
    except Exception as e:
        print(f"Error saving config: {e}")
        return False


def get_tasting_frequency_days(config):
    """Get the number of days between tastings based on frequency setting.
    
    Args:
        config (dict): Configuration data.
        
    Returns:
        int: Number of days between tastings.
    """
    frequency = config.get('user_preferences', {}).get('tasting_frequency', 'weekly')
    
    frequency_map = {
        'weekly': 7,
        'bi-weekly': 14,
        'monthly': 30,
        'custom': config.get('user_preferences', {}).get('custom_interval_days', 7)
    }
    
    return frequency_map.get(frequency, 7)


def get_preferred_days(config):
    """Get list of preferred tasting days.
    
    Args:
        config (dict): Configuration data.
        
    Returns:
        list: List of day names (e.g., ['Friday', 'Saturday']).
    """
    return config.get('user_preferences', {}).get('preferred_days', [])


def get_avoid_dates(config):
    """Get list of dates to avoid.
    
    Args:
        config (dict): Configuration data.
        
    Returns:
        list: List of date strings (YYYY-MM-DD format).
    """
    return config.get('user_preferences', {}).get('avoid_dates', [])


def get_category_preferences(config):
    """Get category preference weights.
    
    Args:
        config (dict): Configuration data.
        
    Returns:
        dict: Category weights (e.g., {'bourbon': 2.0, 'scotch': 1.5}).
    """
    return config.get('user_preferences', {}).get('category_preferences', {})


def get_seasonal_adjustments(config):
    """Check if seasonal adjustments are enabled.
    
    Args:
        config (dict): Configuration data.
        
    Returns:
        bool: True if seasonal adjustments are enabled.
    """
    return config.get('user_preferences', {}).get('seasonal_adjustments', False)


def get_min_days_between_category(config):
    """Get minimum days between tastings of same category.
    
    Args:
        config (dict): Configuration data.
        
    Returns:
        int: Minimum days between same category.
    """
    return config.get('user_preferences', {}).get('min_days_between_category', 0)


def get_default_schedule_weeks(config):
    """Get default schedule duration in weeks.
    
    Args:
        config (dict): Configuration data.
        
    Returns:
        int: Number of weeks for default schedule.
    """
    return config.get('user_preferences', {}).get('default_schedule_weeks', 104)

