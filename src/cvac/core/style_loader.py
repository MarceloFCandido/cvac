"""
Style loader for handling external style configurations.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from copy import deepcopy
import jsonschema

# Try to import yaml, but don't fail if not available
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    yaml = None
    YAML_AVAILABLE = False

# Import default style
from ..style import STYLE_CONFIG as DEFAULT_STYLE


class StyleLoader:
    """Loads and validates style configurations from external files."""
    
    # Basic style schema for validation
    STYLE_SCHEMA = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "font_name": {"type": "string"},
            "font_size": {"type": "number"},
            "name_font_size": {"type": "number"},
            "heading_font_size": {"type": "number"},
            "margins": {
                "type": "object",
                "properties": {
                    "top": {"type": "number"},
                    "bottom": {"type": "number"},
                    "left": {"type": "number"},
                    "right": {"type": "number"}
                }
            },
            "paragraph_spacing": {
                "type": "object",
                "properties": {
                    "before": {"type": "number"},
                    "after": {"type": "number"},
                    "line_spacing": {"type": "number"}
                }
            },
            "bullet_style": {
                "type": "object",
                "properties": {
                    "left_indent": {"type": "number"},
                    "first_line_indent": {"type": "number"},
                    "line_spacing": {"type": "number"},
                    "space_after": {"type": "number"},
                    "space_before": {"type": "number"}
                }
            }
        }
    }
    
    def __init__(self, schema_path: Optional[str] = None):
        """
        Initialize style loader.
        
        Args:
            schema_path: Optional path to custom style schema
        """
        if schema_path:
            with open(schema_path, 'r', encoding='utf-8') as f:
                self.schema = json.load(f)
        else:
            self.schema = self.STYLE_SCHEMA
    
    def detect_format(self, filepath: str) -> str:
        """Detect file format from extension."""
        ext = Path(filepath).suffix.lower()
        if ext == '.json':
            return 'json'
        elif ext in ['.yaml', '.yml']:
            return 'yaml'
        else:
            raise ValueError(f"Unsupported style file format: {ext}")
    
    def load_style(self, filepath: Optional[str] = None) -> Dict[str, Any]:
        """
        Load style configuration from file or return defaults.
        
        Args:
            filepath: Path to style file (JSON or YAML)
            
        Returns:
            Style configuration dictionary
        """
        if filepath is None:
            # Return default style with proper unit conversion
            default = deepcopy(DEFAULT_STYLE)
            return self._convert_units(default)
        
        if not Path(filepath).exists():
            raise FileNotFoundError(f"Style file not found: {filepath}")
        
        format_type = self.detect_format(filepath)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                if format_type == 'json':
                    custom_style = json.load(f)
                else:  # yaml
                    if not YAML_AVAILABLE:
                        raise ImportError("PyYAML is required for YAML file support. Install with: pip install PyYAML")
                    custom_style = yaml.safe_load(f)
        except Exception as e:
            raise ValueError(f"Error loading style file: {e}")
        
        # Validate the loaded style
        self.validate_style(custom_style)
        
        # Merge with defaults (custom values override defaults)
        return self.merge_with_defaults(custom_style)
    
    def validate_style(self, style_config: Dict[str, Any]) -> None:
        """
        Validate style configuration against schema.
        
        Args:
            style_config: Style configuration to validate
            
        Raises:
            jsonschema.ValidationError: If validation fails
        """
        try:
            jsonschema.validate(instance=style_config, schema=self.schema)
        except jsonschema.ValidationError as e:
            raise ValueError(f"Invalid style configuration: {e.message}")
    
    def merge_with_defaults(self, custom_style: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge custom style with default style.
        
        Custom values override defaults, but missing values are filled from defaults.
        
        Args:
            custom_style: Custom style configuration
            
        Returns:
            Merged style configuration
        """
        # Start with a deep copy of defaults
        merged = deepcopy(DEFAULT_STYLE)
        
        # Recursively update with custom values
        self._deep_update(merged, custom_style)
        
        # Convert numeric values to proper units if needed
        merged = self._convert_units(merged)
        
        return merged
    
    def _deep_update(self, base: Dict[str, Any], update: Dict[str, Any]) -> None:
        """Recursively update base dictionary with update dictionary."""
        for key, value in update.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._deep_update(base[key], value)
            else:
                base[key] = value
    
    def _convert_units(self, style: Dict[str, Any]) -> Dict[str, Any]:
        """Convert numeric values to proper docx units."""
        from docx.shared import Pt, Cm, Mm
        
        # Convert margins (assuming mm if just numbers)
        if 'margins' in style:
            for key in ['top', 'bottom', 'left', 'right']:
                if key in style['margins'] and isinstance(style['margins'][key], (int, float)):
                    style['margins'][key] = Mm(style['margins'][key])
        
        # Convert indents (assuming cm if just numbers)
        if 'bullet_style' in style:
            if 'left_indent' in style['bullet_style'] and isinstance(style['bullet_style']['left_indent'], (int, float)):
                style['bullet_style']['left_indent'] = Cm(style['bullet_style']['left_indent'])
            if 'first_line_indent' in style['bullet_style'] and isinstance(style['bullet_style']['first_line_indent'], (int, float)):
                style['bullet_style']['first_line_indent'] = Cm(style['bullet_style']['first_line_indent'])
            
            # Convert space_after and space_before to Pt
            for key in ['space_after', 'space_before']:
                if key in style['bullet_style'] and isinstance(style['bullet_style'][key], (int, float)):
                    style['bullet_style'][key] = Pt(style['bullet_style'][key])
        
        return style

