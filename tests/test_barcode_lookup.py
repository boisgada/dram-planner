#!/usr/bin/env python3
"""
Unit tests for barcode_lookup.py (ENH-002: Barcode Scanning)
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock requests module
import unittest.mock as mock


class TestBarcodeLookup:
    """Test barcode lookup functionality."""
    
    @pytest.mark.parametrize("barcode_input,expected_output", [
        ("1234567890", "1234567890"),
        ("123 456 7890", "1234567890"),
        ("123-456-7890", "1234567890"),
        ("", None),
        (None, None),
    ])
    @mock.patch('barcode_lookup.REQUESTS_AVAILABLE', True)
    @mock.patch('barcode_lookup.requests.get')
    def test_lookup_barcode_normalization(self, mock_get, barcode_input, expected_output):
        """Test barcode normalization (removes spaces and dashes)."""
        import barcode_lookup
        
        if expected_output is None:
            # Test error case
            result = barcode_lookup.lookup_barcode(barcode_input)
            assert result is None
        else:
            # Mock successful API response
            mock_response = mock.Mock()
            mock_response.json.return_value = {
                'status': 1,
                'product': {
                    'product_name': 'Test Product',
                    'brands': 'Test Brand'
                }
            }
            mock_response.raise_for_status = mock.Mock()
            mock_get.return_value = mock_response
            
            result = barcode_lookup.lookup_barcode(barcode_input)
            if result:
                # Verify URL was called with normalized barcode
                mock_get.assert_called_once()
                call_args = mock_get.call_args[0][0]
                assert expected_output in call_args
    
    @mock.patch('barcode_lookup.REQUESTS_AVAILABLE', False)
    def test_lookup_barcode_no_requests(self):
        """Test lookup fails gracefully when requests not available."""
        import barcode_lookup
        result = barcode_lookup.lookup_barcode("1234567890")
        assert result is None
    
    @mock.patch('barcode_lookup.REQUESTS_AVAILABLE', True)
    @mock.patch('barcode_lookup.requests.get')
    def test_lookup_barcode_success(self, mock_get):
        """Test successful barcode lookup."""
        import barcode_lookup
        
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            'status': 1,
            'product': {
                'product_name': 'Test Whisky',
                'product_name_en': 'Test Whisky',
                'brands': 'Test Brand',
                'categories_tags': ['en:whisky'],
                'alcohol_100g': 40.0
            }
        }
        mock_response.raise_for_status = mock.Mock()
        mock_get.return_value = mock_response
        
        result = barcode_lookup.lookup_barcode("1234567890")
        
        assert result is not None
        assert result['name'] == 'Test Whisky'
        assert result['brand'] == 'Test Brand'
        assert result['barcode'] == '1234567890'
    
    @mock.patch('barcode_lookup.REQUESTS_AVAILABLE', True)
    @mock.patch('barcode_lookup.requests.get')
    def test_lookup_barcode_not_found(self, mock_get):
        """Test barcode not found in API."""
        import barcode_lookup
        
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            'status': 0,
            'product': None
        }
        mock_response.raise_for_status = mock.Mock()
        mock_get.return_value = mock_response
        
        result = barcode_lookup.lookup_barcode("1234567890")
        assert result is None
    
    @mock.patch('barcode_lookup.REQUESTS_AVAILABLE', True)
    @mock.patch('barcode_lookup.requests.get')
    def test_lookup_barcode_api_error(self, mock_get):
        """Test API connection error handling."""
        import barcode_lookup
        
        mock_get.side_effect = Exception("Connection error")
        
        result = barcode_lookup.lookup_barcode("1234567890")
        assert result is None

