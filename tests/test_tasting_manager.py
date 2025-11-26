#!/usr/bin/env python3
"""Unit tests for tasting_manager.py"""

import unittest
import json
import tempfile
import os
from datetime import datetime
import sys

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tasting_manager import (
    load_json,
    save_json,
    record_tasting
)


class TestTastingManager(unittest.TestCase):
    """Test cases for tasting manager functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_collection = {
            'bottles': [
                {
                    'id': 1,
                    'name': 'Test Bourbon',
                    'category': 'bourbon',
                    'tasted': False,
                    'rating': None,
                    'tasting_notes': ''
                }
            ],
            'metadata': {'total_bottles': 1, 'last_updated': ''}
        }
    
    def test_load_json_valid(self):
        """Test loading a valid JSON file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.test_collection, f)
            temp_path = f.name
        
        try:
            result = load_json(temp_path)
            self.assertIsNotNone(result)
            self.assertEqual(len(result['bottles']), 1)
        finally:
            os.unlink(temp_path)
    
    def test_load_json_not_found(self):
        """Test loading a non-existent file."""
        result = load_json('nonexistent.json')
        self.assertIsNone(result)
    
    def test_save_json(self):
        """Test saving JSON data."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            result = save_json(self.test_collection, temp_path)
            self.assertTrue(result)
            self.assertTrue(os.path.exists(temp_path))
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_record_tasting_valid(self):
        """Test recording a valid tasting."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.test_collection, f)
            temp_path = f.name
        
        try:
            result = record_tasting(temp_path, 1, 7.5, "Great taste!")
            self.assertTrue(result)
            
            # Verify the tasting was recorded
            data = load_json(temp_path)
            bottle = data['bottles'][0]
            self.assertTrue(bottle['tasted'])
            self.assertEqual(bottle['rating'], 7.5)
            self.assertEqual(bottle['tasting_notes'], "Great taste!")
        finally:
            os.unlink(temp_path)
    
    def test_record_tasting_invalid_id(self):
        """Test recording tasting with invalid bottle ID."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.test_collection, f)
            temp_path = f.name
        
        try:
            result = record_tasting(temp_path, 999, 7.5, "Notes")
            self.assertFalse(result)
        finally:
            os.unlink(temp_path)
    
    def test_record_tasting_invalid_rating(self):
        """Test recording tasting with invalid rating."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.test_collection, f)
            temp_path = f.name
        
        try:
            result = record_tasting(temp_path, 1, 15, "Notes")  # Rating > 10
            self.assertFalse(result)
            
            result = record_tasting(temp_path, 1, -1, "Notes")  # Rating < 0
            self.assertFalse(result)
        finally:
            os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()

