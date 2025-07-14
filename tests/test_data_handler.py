"""
Tests for data_handler module.
"""

import pytest
import json
import yaml
import tempfile
import os
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from cvac.core.data_handler import DataHandler


@pytest.fixture
def sample_cv_data():
    """Sample CV data for testing."""
    return {
        "personalInfo": {
            "firstName": "Test",
            "lastName": "User",
            "email": "test@example.com",
            "location": {
                "city": "Test City",
                "country": "Test Country"
            }
        },
        "workExperience": [
            {
                "company": "Test Company",
                "position": "Test Position",
                "startDate": "2020-01"
            }
        ],
        "education": [
            {
                "institution": "Test University",
                "degree": "Test Degree",
                "graduationDate": "2020-05"
            }
        ]
    }


@pytest.fixture
def temp_files(sample_cv_data):
    """Create temporary JSON and YAML files."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(sample_cv_data, f)
        json_file = f.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(sample_cv_data, f)
        yaml_file = f.name
    
    yield json_file, yaml_file
    
    # Cleanup
    os.unlink(json_file)
    os.unlink(yaml_file)


def test_detect_format_by_extension():
    """Test format detection by file extension."""
    handler = DataHandler()
    
    assert handler.detect_format("test.json") == "json"
    assert handler.detect_format("test.JSON") == "json"
    assert handler.detect_format("test.yaml") == "yaml"
    assert handler.detect_format("test.yml") == "yaml"
    assert handler.detect_format("test.YAML") == "yaml"


def test_load_json_data(temp_files):
    """Test loading JSON data."""
    json_file, _ = temp_files
    handler = DataHandler()
    
    data = handler.load_data(json_file)
    assert data["personalInfo"]["firstName"] == "Test"
    assert data["personalInfo"]["email"] == "test@example.com"


def test_load_yaml_data(temp_files):
    """Test loading YAML data."""
    _, yaml_file = temp_files
    handler = DataHandler()
    
    data = handler.load_data(yaml_file)
    assert data["personalInfo"]["firstName"] == "Test"
    assert data["personalInfo"]["email"] == "test@example.com"


def test_validate_valid_data(sample_cv_data):
    """Test validation of valid data."""
    handler = DataHandler()
    # Should not raise any exception
    handler.validate_data(sample_cv_data)


def test_validate_invalid_data():
    """Test validation of invalid data."""
    handler = DataHandler()
    
    # Missing required fields
    invalid_data = {
        "personalInfo": {
            "firstName": "Test"
            # Missing required fields
        }
    }
    
    with pytest.raises(Exception):  # Will be jsonschema.ValidationError
        handler.validate_data(invalid_data)


def test_save_data_json(sample_cv_data):
    """Test saving data as JSON."""
    handler = DataHandler()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        output_file = f.name
    
    try:
        handler.save_data(sample_cv_data, output_file, format_type='json')
        
        # Read back and verify
        with open(output_file, 'r') as f:
            loaded_data = json.load(f)
        
        assert loaded_data == sample_cv_data
    finally:
        os.unlink(output_file)


def test_save_data_yaml(sample_cv_data):
    """Test saving data as YAML."""
    handler = DataHandler()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        output_file = f.name
    
    try:
        handler.save_data(sample_cv_data, output_file, format_type='yaml')
        
        # Read back and verify
        with open(output_file, 'r') as f:
            loaded_data = yaml.safe_load(f)
        
        assert loaded_data == sample_cv_data
    finally:
        os.unlink(output_file)


def test_file_not_found():
    """Test handling of non-existent file."""
    handler = DataHandler()
    
    with pytest.raises(FileNotFoundError):
        handler.load_data("non_existent_file.json")
