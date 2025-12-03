"""
Shared pytest fixtures and configuration for Dram Planner tests.
"""

import pytest
import tempfile
import json
import os
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_collection():
    """Sample collection data for testing."""
    return {
        'bottles': [
            {
                'id': 1,
                'name': 'Test Bourbon',
                'category': 'bourbon',
                'tasted': False,
                'rating': None,
                'tasting_notes': ''
            },
            {
                'id': 2,
                'name': 'Test Scotch',
                'category': 'scotch',
                'tasted': False,
                'rating': None,
                'tasting_notes': ''
            },
            {
                'id': 3,
                'name': 'Test Irish',
                'category': 'irish',
                'tasted': True,
                'rating': 8.5,
                'tasting_notes': 'Great flavor'
            }
        ],
        'metadata': {
            'total_bottles': 3,
            'last_updated': '2024-01-01T00:00:00'
        }
    }


@pytest.fixture
def collection_file(temp_dir, sample_collection):
    """Create a temporary collection JSON file."""
    filepath = os.path.join(temp_dir, 'collection.json')
    with open(filepath, 'w') as f:
        json.dump(sample_collection, f)
    return filepath


@pytest.fixture
def default_config():
    """Default configuration data for testing."""
    return {
        "user_preferences": {
            "tasting_frequency": "weekly",
            "custom_interval_days": 7,
            "preferred_days": [],
            "avoid_dates": [],
            "category_preferences": {},
            "seasonal_adjustments": False,
            "min_days_between_category": 0,
            "default_schedule_weeks": 104
        },
        "import_sources": {
            "open_food_facts": {
                "enabled": False,
                "api_url": "https://world.openfoodfacts.org/api/v0/product/{}.json"
            }
        },
        "data_files": {
            "collection_file": "collection.json",
            "schedule_file": "tasting_schedule.json"
        }
    }


@pytest.fixture
def config_file(temp_dir, default_config):
    """Create a temporary config JSON file."""
    filepath = os.path.join(temp_dir, 'config.json')
    with open(filepath, 'w') as f:
        json.dump(default_config, f, indent=2)
    return filepath


@pytest.fixture
def empty_collection():
    """Empty collection data for testing."""
    return {
        'bottles': [],
        'metadata': {
            'total_bottles': 0,
            'last_updated': ''
        }
    }

