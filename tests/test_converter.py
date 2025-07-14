"""
Tests for format conversion functionality.
"""

import pytest
import json
import yaml
import tempfile
import os
import sys
import subprocess

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from cvac.core.data_handler import DataHandler


@pytest.fixture
def sample_data():
    """Sample data for conversion tests."""
    return {
        "personalInfo": {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john@example.com",
            "location": {"city": "Boston", "country": "USA"}
        },
        "workExperience": [{
            "company": "Tech Corp",
            "position": "Developer",
            "startDate": "2020-01"
        }],
        "education": [{
            "institution": "MIT",
            "degree": "BS",
            "graduationDate": "2019-05"
        }]
    }


def test_json_to_yaml_conversion(sample_data):
    """Test converting JSON to YAML."""
    handler = DataHandler()
    
    # Create temp JSON file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(sample_data, f)
        json_file = f.name
    
    # Create temp YAML file path
    yaml_file = json_file.replace('.json', '.yaml')
    
    try:
        # Load from JSON
        loaded_data = handler.load_data(json_file)
        
        # Save as YAML
        handler.save_data(loaded_data, yaml_file, format_type='yaml')
        
        # Load the YAML and verify
        with open(yaml_file, 'r') as f:
            yaml_data = yaml.safe_load(f)
        
        assert yaml_data == sample_data
        
    finally:
        os.unlink(json_file)
        if os.path.exists(yaml_file):
            os.unlink(yaml_file)


def test_yaml_to_json_conversion(sample_data):
    """Test converting YAML to JSON."""
    handler = DataHandler()
    
    # Create temp YAML file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(sample_data, f)
        yaml_file = f.name
    
    # Create temp JSON file path
    json_file = yaml_file.replace('.yaml', '.json')
    
    try:
        # Load from YAML
        loaded_data = handler.load_data(yaml_file)
        
        # Save as JSON
        handler.save_data(loaded_data, json_file, format_type='json')
        
        # Load the JSON and verify
        with open(json_file, 'r') as f:
            json_data = json.load(f)
        
        assert json_data == sample_data
        
    finally:
        os.unlink(yaml_file)
        if os.path.exists(json_file):
            os.unlink(json_file)


def test_convert_preserves_unicode():
    """Test that conversion preserves unicode characters."""
    handler = DataHandler()
    
    data_with_unicode = {
        "personalInfo": {
            "firstName": "José",
            "lastName": "García",
            "email": "jose@ejemplo.com",
            "location": {"city": "São Paulo", "country": "Brasil"}
        },
        "workExperience": [],
        "education": []
    }
    
    # Test JSON -> YAML -> JSON
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(data_with_unicode, f, ensure_ascii=False)
        json_file = f.name
    
    yaml_file = json_file.replace('.json', '.yaml')
    json_file2 = yaml_file.replace('.yaml', '_2.json')
    
    try:
        # JSON -> YAML
        data1 = handler.load_data(json_file)
        handler.save_data(data1, yaml_file)
        
        # YAML -> JSON
        data2 = handler.load_data(yaml_file)
        handler.save_data(data2, json_file2)
        
        # Verify data integrity
        with open(json_file2, 'r', encoding='utf-8') as f:
            final_data = json.load(f)
        
        assert final_data["personalInfo"]["firstName"] == "José"
        assert final_data["personalInfo"]["location"]["city"] == "São Paulo"
        
    finally:
        for f in [json_file, yaml_file, json_file2]:
            if os.path.exists(f):
                os.unlink(f)


def test_pretty_print_json():
    """Test pretty printing JSON output."""
    handler = DataHandler()
    
    simple_data = {"a": 1, "b": [2, 3], "c": {"d": 4}}
    
    # Test with pretty=True
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        pretty_file = f.name
    
    try:
        handler.save_data(simple_data, pretty_file, format_type='json', pretty=True)
        
        with open(pretty_file, 'r') as f:
            content = f.read()
        
        # Pretty printed JSON should have newlines and indentation
        assert '\n' in content
        assert '  ' in content  # indentation
        
    finally:
        os.unlink(pretty_file)
