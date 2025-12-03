#!/usr/bin/env python3
"""
Unit tests for import_manager.py (ENH-003: Enhanced External Import)
"""

import pytest
import json
import csv
import os
import sys
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import import_manager


class TestValidateBottleData:
    """Test bottle data validation."""
    
    def test_validate_bottle_data_valid(self):
        """Test validation of valid bottle data."""
        bottle_data = {
            'name': 'Test Bottle',
            'category': 'bourbon',
            'abv': 40.0
        }
        is_valid, errors = import_manager.validate_bottle_data(bottle_data)
        assert is_valid is True
        assert len(errors) == 0
    
    def test_validate_bottle_data_missing_name(self):
        """Test validation fails when name is missing."""
        bottle_data = {
            'category': 'bourbon'
        }
        is_valid, errors = import_manager.validate_bottle_data(bottle_data)
        assert is_valid is False
        assert any('name' in error.lower() for error in errors)
    
    def test_validate_bottle_data_missing_category(self):
        """Test validation fails when category is missing."""
        bottle_data = {
            'name': 'Test Bottle'
        }
        is_valid, errors = import_manager.validate_bottle_data(bottle_data)
        assert is_valid is False
        assert any('category' in error.lower() for error in errors)
    
    def test_validate_bottle_data_invalid_abv_high(self):
        """Test validation fails when ABV is too high."""
        bottle_data = {
            'name': 'Test Bottle',
            'category': 'bourbon',
            'abv': 150.0
        }
        is_valid, errors = import_manager.validate_bottle_data(bottle_data, row_num=1)
        assert is_valid is False
        assert any('abv' in error.lower() for error in errors)
    
    def test_validate_bottle_data_invalid_abv_negative(self):
        """Test validation fails when ABV is negative."""
        bottle_data = {
            'name': 'Test Bottle',
            'category': 'bourbon',
            'abv': -10.0
        }
        is_valid, errors = import_manager.validate_bottle_data(bottle_data)
        assert is_valid is False
    
    def test_validate_bottle_data_invalid_date_format(self):
        """Test validation fails with invalid date format."""
        bottle_data = {
            'name': 'Test Bottle',
            'category': 'bourbon',
            'purchase_date': '01-01-2024'  # Wrong format
        }
        is_valid, errors = import_manager.validate_bottle_data(bottle_data, row_num=1)
        assert is_valid is False
        assert any('date' in error.lower() for error in errors)
    
    def test_validate_bottle_data_valid_date_format(self):
        """Test validation passes with valid date format."""
        bottle_data = {
            'name': 'Test Bottle',
            'category': 'bourbon',
            'purchase_date': '2024-01-01'
        }
        is_valid, errors = import_manager.validate_bottle_data(bottle_data)
        assert is_valid is True


class TestNormalizeBottleData:
    """Test bottle data normalization."""
    
    def test_normalize_bottle_data_complete(self):
        """Test normalization of complete bottle data."""
        raw_data = {
            'name': '  Test Bottle  ',
            'category': 'BOURBON',
            'abv': '40.0',
            'price_paid': '50.00',
            'notes': 'Test notes'
        }
        normalized = import_manager.normalize_bottle_data(raw_data)
        
        assert normalized['name'] == 'Test Bottle'
        assert normalized['category'] == 'bourbon'
        assert normalized['abv'] == 40.0
        assert normalized['price_paid'] == 50.0
    
    def test_normalize_bottle_data_minimal(self):
        """Test normalization with minimal data."""
        raw_data = {
            'name': 'Test Bottle',
            'category': 'bourbon'
        }
        normalized = import_manager.normalize_bottle_data(raw_data)
        
        assert normalized['name'] == 'Test Bottle'
        assert normalized['category'] == 'bourbon'
        assert normalized['abv'] == 0.0
        assert normalized['price_paid'] == 0.0


class TestImportFromCSV:
    """Test CSV import functionality."""
    
    def test_import_from_csv_valid(self, temp_dir):
        """Test importing valid CSV file."""
        csv_file = os.path.join(temp_dir, 'bottles.csv')
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'category', 'abv'])
            writer.writerow(['Test Bourbon', 'bourbon', '40.0'])
            writer.writerow(['Test Scotch', 'scotch', '43.0'])
        
        bottles, errors, warnings = import_manager.import_from_csv(csv_file)
        
        assert len(bottles) == 2
        assert len(errors) == 0
        assert bottles[0]['name'] == 'Test Bourbon'
    
    def test_import_from_csv_not_found(self):
        """Test importing non-existent CSV file."""
        bottles, errors, warnings = import_manager.import_from_csv('nonexistent.csv')
        assert len(bottles) == 0
        assert len(errors) > 0
    
    def test_import_from_csv_with_errors(self, temp_dir):
        """Test CSV import with validation errors."""
        csv_file = os.path.join(temp_dir, 'bottles.csv')
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'category'])
            writer.writerow(['Test Bourbon', ''])  # Missing category
            writer.writerow(['', 'bourbon'])  # Missing name
        
        bottles, errors, warnings = import_manager.import_from_csv(csv_file)
        assert len(errors) > 0


class TestImportFromJSON:
    """Test JSON import functionality."""
    
    def test_import_from_json_valid_array(self, temp_dir):
        """Test importing valid JSON array."""
        json_file = os.path.join(temp_dir, 'bottles.json')
        data = [
            {'name': 'Test Bourbon', 'category': 'bourbon'},
            {'name': 'Test Scotch', 'category': 'scotch'}
        ]
        with open(json_file, 'w') as f:
            json.dump(data, f)
        
        bottles, errors, warnings = import_manager.import_from_json(json_file)
        assert len(bottles) == 2
        assert len(errors) == 0
    
    def test_import_from_json_valid_object(self, temp_dir):
        """Test importing valid JSON object with bottles array."""
        json_file = os.path.join(temp_dir, 'bottles.json')
        data = {
            'bottles': [
                {'name': 'Test Bourbon', 'category': 'bourbon'}
            ]
        }
        with open(json_file, 'w') as f:
            json.dump(data, f)
        
        bottles, errors, warnings = import_manager.import_from_json(json_file)
        assert len(bottles) == 1
    
    def test_import_from_json_not_found(self):
        """Test importing non-existent JSON file."""
        bottles, errors, warnings = import_manager.import_from_json('nonexistent.json')
        assert len(bottles) == 0
        assert len(errors) > 0

