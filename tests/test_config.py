#!/usr/bin/env python3
"""
Unit tests for config.py (ENH-001: User Preferences)
"""

import pytest
import json
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config


class TestConfigLoadSave:
    """Test configuration loading and saving."""
    
    def test_load_config_default_creation(self, temp_dir):
        """Test that loading non-existent config creates default config."""
        config_path = os.path.join(temp_dir, 'config.json')
        result = config.load_config(config_path)
        
        assert result is not None
        assert 'user_preferences' in result
        assert os.path.exists(config_path)
    
    def test_load_config_existing_file(self, config_file):
        """Test loading existing config file."""
        result = config.load_config(config_file)
        assert result is not None
        assert 'user_preferences' in result
    
    def test_save_config(self, temp_dir, default_config):
        """Test saving configuration."""
        config_path = os.path.join(temp_dir, 'test_config.json')
        result = config.save_config(default_config, config_path)
        
        assert result is True
        assert os.path.exists(config_path)
        
        # Verify content
        with open(config_path, 'r') as f:
            saved = json.load(f)
        assert saved == default_config
    
    def test_load_config_merges_with_defaults(self, temp_dir):
        """Test that loading config merges with defaults."""
        partial_config = {
            "user_preferences": {
                "tasting_frequency": "bi-weekly"
            }
        }
        config_path = os.path.join(temp_dir, 'partial_config.json')
        with open(config_path, 'w') as f:
            json.dump(partial_config, f)
        
        result = config.load_config(config_path)
        assert result['user_preferences']['tasting_frequency'] == "bi-weekly"
        # Should have other defaults
        assert 'custom_interval_days' in result['user_preferences']


class TestTastingFrequency:
    """Test tasting frequency functions."""
    
    def test_get_tasting_frequency_days_weekly(self, default_config):
        """Test weekly frequency returns 7 days."""
        result = config.get_tasting_frequency_days(default_config)
        assert result == 7
    
    def test_get_tasting_frequency_days_biweekly(self, default_config):
        """Test bi-weekly frequency returns 14 days."""
        default_config['user_preferences']['tasting_frequency'] = "bi-weekly"
        result = config.get_tasting_frequency_days(default_config)
        assert result == 14
    
    def test_get_tasting_frequency_days_monthly(self, default_config):
        """Test monthly frequency returns 30 days."""
        default_config['user_preferences']['tasting_frequency'] = "monthly"
        result = config.get_tasting_frequency_days(default_config)
        assert result == 30
    
    def test_get_tasting_frequency_days_custom(self, default_config):
        """Test custom frequency returns custom_interval_days."""
        default_config['user_preferences']['tasting_frequency'] = "custom"
        default_config['user_preferences']['custom_interval_days'] = 10
        result = config.get_tasting_frequency_days(default_config)
        assert result == 10


class TestPreferredDays:
    """Test preferred days functions."""
    
    def test_get_preferred_days_empty(self, default_config):
        """Test empty preferred days list."""
        result = config.get_preferred_days(default_config)
        assert result == []
    
    def test_get_preferred_days_list(self, default_config):
        """Test preferred days list."""
        default_config['user_preferences']['preferred_days'] = ['Friday', 'Saturday']
        result = config.get_preferred_days(default_config)
        assert result == ['Friday', 'Saturday']


class TestAvoidDates:
    """Test avoid dates functions."""
    
    def test_get_avoid_dates_empty(self, default_config):
        """Test empty avoid dates list."""
        result = config.get_avoid_dates(default_config)
        assert result == []
    
    def test_get_avoid_dates_list(self, default_config):
        """Test avoid dates list."""
        dates = ['2024-12-25', '2024-01-01']
        default_config['user_preferences']['avoid_dates'] = dates
        result = config.get_avoid_dates(default_config)
        assert result == dates


class TestCategoryPreferences:
    """Test category preference functions."""
    
    def test_get_category_preferences_empty(self, default_config):
        """Test empty category preferences."""
        result = config.get_category_preferences(default_config)
        assert result == {}
    
    def test_get_category_preferences_dict(self, default_config):
        """Test category preferences dict."""
        prefs = {'bourbon': 2.0, 'scotch': 1.5}
        default_config['user_preferences']['category_preferences'] = prefs
        result = config.get_category_preferences(default_config)
        assert result == prefs


class TestSeasonalAdjustments:
    """Test seasonal adjustment functions."""
    
    def test_get_seasonal_adjustments_false(self, default_config):
        """Test seasonal adjustments disabled."""
        result = config.get_seasonal_adjustments(default_config)
        assert result is False
    
    def test_get_seasonal_adjustments_true(self, default_config):
        """Test seasonal adjustments enabled."""
        default_config['user_preferences']['seasonal_adjustments'] = True
        result = config.get_seasonal_adjustments(default_config)
        assert result is True


class TestMinDaysBetweenCategory:
    """Test minimum days between category functions."""
    
    def test_get_min_days_between_category_default(self, default_config):
        """Test default minimum days."""
        result = config.get_min_days_between_category(default_config)
        assert result == 0
    
    def test_get_min_days_between_category_custom(self, default_config):
        """Test custom minimum days."""
        default_config['user_preferences']['min_days_between_category'] = 3
        result = config.get_min_days_between_category(default_config)
        assert result == 3


class TestDefaultScheduleWeeks:
    """Test default schedule weeks functions."""
    
    def test_get_default_schedule_weeks_default(self, default_config):
        """Test default schedule weeks."""
        result = config.get_default_schedule_weeks(default_config)
        assert result == 104
    
    def test_get_default_schedule_weeks_custom(self, default_config):
        """Test custom schedule weeks."""
        default_config['user_preferences']['default_schedule_weeks'] = 52
        result = config.get_default_schedule_weeks(default_config)
        assert result == 52

