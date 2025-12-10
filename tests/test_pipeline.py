# tests/test_pipeline.py
"""
Unit tests for the CI/CD ML Pipeline
"""
import os
import sys
import pytest
import json
import shutil
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_manager import (
    get_data_count,
    increment_data_count,
    reset_data_count,
    get_current_version,
    increment_version
)
from config import DATA_COUNTER_FILE


class TestDataManager:
    """Test data management functions"""
    
    def setup_method(self):
        """Setup test environment"""
        # Backup original counter if it exists
        if os.path.exists(DATA_COUNTER_FILE):
            shutil.copy(DATA_COUNTER_FILE, DATA_COUNTER_FILE + '.backup')
        
        # Create test counter
        test_data = {"count": 0, "last_trained": None, "current_version": 1}
        with open(DATA_COUNTER_FILE, 'w') as f:
            json.dump(test_data, f)
    
    def teardown_method(self):
        """Cleanup after tests"""
        # Restore original counter
        if os.path.exists(DATA_COUNTER_FILE + '.backup'):
            shutil.move(DATA_COUNTER_FILE + '.backup', DATA_COUNTER_FILE)
    
    def test_get_data_count_initial(self):
        """Test getting initial data count"""
        count = get_data_count()
        assert count == 0
    
    def test_increment_data_count(self):
        """Test incrementing data count"""
        count = increment_data_count(5)
        assert count == 5
        
        count = increment_data_count(10)
        assert count == 15
    
    def test_reset_data_count(self):
        """Test resetting data count"""
        increment_data_count(100)
        reset_data_count()
        
        count = get_data_count()
        assert count == 0
    
    def test_version_management(self):
        """Test version increment"""
        initial_version = get_current_version()
        assert initial_version == 1
        
        new_version = increment_version()
        assert new_version == 2
        
        current = get_current_version()
        assert current == 2


class TestConfiguration:
    """Test configuration constants"""
    
    def test_threshold_value(self):
        """Test that threshold is set correctly"""
        from config import NEW_DATA_THRESHOLD
        assert NEW_DATA_THRESHOLD == 200
    
    def test_directories_exist(self):
        """Test that required directories are created"""
        from config import NEW_DATA_DIR, MODEL_DIR
        assert os.path.exists(NEW_DATA_DIR)
        assert os.path.exists(MODEL_DIR)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
