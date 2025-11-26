#!/usr/bin/env python3
"""Unit tests for schedule_generator.py"""

import unittest
import json
import tempfile
import os
from datetime import datetime, timedelta
import sys

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schedule_generator import (
    load_collection,
    save_collection,
    categorize_bottles,
    generate_schedule,
    save_schedule
)


class TestScheduleGenerator(unittest.TestCase):
    """Test cases for schedule generator functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_collection = {
            'bottles': [
                {'id': 1, 'name': 'Test Bourbon', 'category': 'bourbon', 'tasted': False},
                {'id': 2, 'name': 'Test Scotch', 'category': 'scotch', 'tasted': False},
                {'id': 3, 'name': 'Test Irish', 'category': 'irish', 'tasted': True}
            ],
            'metadata': {'total_bottles': 3, 'last_updated': ''}
        }
    
    def test_load_collection_valid(self):
        """Test loading a valid collection file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.test_collection, f)
            temp_path = f.name
        
        try:
            result = load_collection(temp_path)
            self.assertIsNotNone(result)
            self.assertEqual(len(result['bottles']), 3)
        finally:
            os.unlink(temp_path)
    
    def test_load_collection_not_found(self):
        """Test loading a non-existent file."""
        result = load_collection('nonexistent.json')
        self.assertIsNone(result)
    
    def test_save_collection(self):
        """Test saving a collection."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            result = save_collection(self.test_collection, temp_path)
            self.assertTrue(result)
            self.assertTrue(os.path.exists(temp_path))
            
            # Verify content
            with open(temp_path, 'r') as f:
                saved = json.load(f)
            self.assertEqual(len(saved['bottles']), 3)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_categorize_bottles(self):
        """Test categorizing bottles."""
        categories = categorize_bottles(self.test_collection['bottles'])
        self.assertIn('bourbon', categories)
        self.assertIn('scotch', categories)
        self.assertIn('irish', categories)
        self.assertEqual(len(categories['bourbon']), 1)
    
    def test_generate_schedule_basic(self):
        """Test basic schedule generation."""
        schedule = generate_schedule(self.test_collection, weeks=10)
        self.assertEqual(len(schedule), 10)
        self.assertEqual(schedule[0]['week'], 1)
        self.assertIn('date', schedule[0])
        self.assertIn('bottle_id', schedule[0])
    
    def test_generate_schedule_prioritizes_untasted(self):
        """Test that untasted bottles are scheduled first."""
        schedule = generate_schedule(self.test_collection, weeks=10)
        # First entries should be untasted (IDs 1 and 2)
        untasted_ids = {1, 2}
        first_bottles = [entry['bottle_id'] for entry in schedule[:2]]
        self.assertTrue(any(bid in untasted_ids for bid in first_bottles))
    
    def test_generate_schedule_invalid_collection(self):
        """Test schedule generation with invalid collection."""
        result = generate_schedule({}, weeks=10)
        self.assertEqual(result, [])
        
        result = generate_schedule(None, weeks=10)
        self.assertEqual(result, [])
    
    def test_generate_schedule_invalid_weeks(self):
        """Test schedule generation with invalid weeks."""
        result = generate_schedule(self.test_collection, weeks=0)
        self.assertEqual(result, [])
        
        result = generate_schedule(self.test_collection, weeks=-1)
        self.assertEqual(result, [])
    
    def test_save_schedule(self):
        """Test saving a schedule."""
        schedule = generate_schedule(self.test_collection, weeks=5)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            result = save_schedule(schedule, temp_path)
            self.assertTrue(result)
            self.assertTrue(os.path.exists(temp_path))
            
            # Verify content
            with open(temp_path, 'r') as f:
                saved = json.load(f)
            self.assertEqual(saved['total_weeks'], 5)
            self.assertEqual(len(saved['schedule']), 5)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()

