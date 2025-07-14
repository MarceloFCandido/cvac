"""
Tests for style_loader module.
"""

import pytest
import json
import yaml
import tempfile
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from cvac.core.style_loader import StyleLoader
from cvac.style import STYLE_CONFIG as DEFAULT_STYLE


@pytest.fixture
def custom_style():
    """Custom style configuration for testing."""
    return {
        "font_name": "Times New Roman",
        "font_size": 12,
        "name_font_size": 20,
        "margins": {
            "top": 25,
            "bottom": 25,
            "left": 30,
            "right": 30
        }
    }


def test_load_default_style():
    """Test loading default style when no file provided."""
    loader = StyleLoader()
    style = loader.load_style()
    
    # Should return default style
    assert style["font_name"] == DEFAULT_STYLE["font_name"]
    assert style["font_size"] == DEFAULT_STYLE["font_size"]


def test_load_json_style(custom_style):
    """Test loading style from JSON file."""
    loader = StyleLoader()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(custom_style, f)
        style_file = f.name
    
    try:
        loaded_style = loader.load_style(style_file)
        
        # Custom values should override defaults
        assert loaded_style["font_name"] == "Times New Roman"
        assert loaded_style["font_size"] == 12
        assert loaded_style["name_font_size"] == 20
        
        # Default values should still be present
        assert "paragraph_spacing" in loaded_style
        assert "bullet_style" in loaded_style
        
    finally:
        os.unlink(style_file)


def test_load_yaml_style(custom_style):
    """Test loading style from YAML file."""
    loader = StyleLoader()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(custom_style, f)
        style_file = f.name
    
    try:
        loaded_style = loader.load_style(style_file)
        
        # Custom values should override defaults
        assert loaded_style["font_name"] == "Times New Roman"
        assert loaded_style["font_size"] == 12
        
    finally:
        os.unlink(style_file)


def test_style_validation():
    """Test style validation."""
    loader = StyleLoader()
    
    # Valid style should pass
    valid_style = {"font_name": "Arial", "font_size": 10}
    loader.validate_style(valid_style)  # Should not raise
    
    # Invalid style should fail
    invalid_style = {"font_name": 123}  # Wrong type
    with pytest.raises(ValueError):
        loader.validate_style(invalid_style)


def test_merge_with_defaults():
    """Test merging custom style with defaults."""
    loader = StyleLoader()
    
    partial_style = {
        "font_name": "Georgia",
        "margins": {
            "top": 30  # Only override top margin
        }
    }
    
    merged = loader.merge_with_defaults(partial_style)
    
    # Custom values
    assert merged["font_name"] == "Georgia"
    assert merged["margins"]["top"].mm == 30  # Will be converted to Mm object
    
    # Default values preserved
    assert merged["font_size"] == DEFAULT_STYLE["font_size"]
    assert "bottom" in merged["margins"]
    assert "left" in merged["margins"]
    assert "right" in merged["margins"]


def test_unit_conversion():
    """Test automatic unit conversion for numeric values."""
    loader = StyleLoader()
    
    style_with_numbers = {
        "margins": {
            "top": 25,  # Should be converted to Mm(25)
            "bottom": 20
        },
        "bullet_style": {
            "left_indent": 0.5,  # Should be converted to Cm(0.5)
            "space_after": 5  # Should be converted to Pt(5)
        }
    }
    
    merged = loader.merge_with_defaults(style_with_numbers)
    
    # Check conversions
    assert hasattr(merged["margins"]["top"], "mm")
    assert hasattr(merged["bullet_style"]["left_indent"], "cm")
    assert hasattr(merged["bullet_style"]["space_after"], "pt")


def test_file_not_found():
    """Test handling of non-existent style file."""
    loader = StyleLoader()
    
    with pytest.raises(FileNotFoundError):
        loader.load_style("non_existent_style.json")


def test_invalid_json_style():
    """Test handling of invalid JSON in style file."""
    loader = StyleLoader()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write("{ invalid json }")
        style_file = f.name
    
    try:
        with pytest.raises(ValueError):
            loader.load_style(style_file)
    finally:
        os.unlink(style_file)
