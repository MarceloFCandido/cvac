"""
Data handler for loading and validating CV data from JSON/YAML files.
"""

import json
import os
from pathlib import Path
import jsonschema
from typing import Dict, Any, Optional, Literal

# Try to import yaml, but don't fail if not available
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    yaml = None
    YAML_AVAILABLE = False


class DataHandler:
    """Handles loading, validation, and saving of CV data in JSON/YAML formats."""
    
    def __init__(self, schema_path: Optional[str] = None):
        """
        Initialize data handler with optional custom schema path.
        
        Args:
            schema_path: Path to JSON schema file. If None, uses default CV schema.
        """
        if schema_path is None:
            # Try multiple strategies to find the schema
            schema_path = self._find_default_schema()
        
        self.schema_path = Path(schema_path)
        self.schema = self._load_schema()
    
    def _find_default_schema(self) -> Path:
        """Find the default CV schema file."""
        schema_filename = 'cv.schema.json'
        
        # Strategy 1: Look relative to this file (development mode)
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent.parent.parent
        schema_path = project_root / 'schema' / schema_filename
        if schema_path.exists():
            return schema_path
        
        # Strategy 2: Look in current working directory
        cwd_schema = Path.cwd() / 'schema' / schema_filename
        if cwd_schema.exists():
            return cwd_schema
        
        # Strategy 3: Look in parent directories of CWD
        current = Path.cwd()
        for _ in range(3):  # Look up to 3 levels
            potential_schema = current / 'schema' / schema_filename
            if potential_schema.exists():
                return potential_schema
            current = current.parent
        
        # If we still can't find it, raise an error with helpful message
        raise FileNotFoundError(
            f"Cannot find {schema_filename}. Please ensure you're running from the project directory "
            f"or specify the schema path explicitly."
        )
    
    def _load_schema(self) -> Dict[str, Any]:
        """Load JSON schema for validation."""
        try:
            with open(self.schema_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Schema file not found: {self.schema_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON schema: {e}")
    
    def detect_format(self, filepath: str) -> Literal['json', 'yaml']:
        """
        Detect file format based on extension.
        
        Args:
            filepath: Path to the file
            
        Returns:
            'json' or 'yaml'
            
        Raises:
            ValueError: If file extension is not recognized
        """
        path = Path(filepath)
        ext = path.suffix.lower()
        
        if ext in ['.json']:
            return 'json'
        elif ext in ['.yaml', '.yml']:
            return 'yaml'
        else:
            # Try to detect by content
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Try JSON first
                    try:
                        json.loads(content)
                        return 'json'
                    except json.JSONDecodeError:
                        # Try YAML
                        if not YAML_AVAILABLE:
                            raise ValueError("Cannot determine format and PyYAML not available")
                        yaml.safe_load(content)
                        return 'yaml'
            except Exception:
                raise ValueError(f"Cannot determine format for file: {filepath}")
    
    def load_data(self, filepath: str) -> Dict[str, Any]:
        """
        Load data from JSON or YAML file.
        
        Args:
            filepath: Path to the data file
            
        Returns:
            Loaded data as dictionary
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        format_type = self.detect_format(filepath)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                if format_type == 'json':
                    return json.load(f)
                else:  # yaml
                    if not YAML_AVAILABLE:
                        raise ImportError("PyYAML is required for YAML file support. Install with: pip install PyYAML")
                    return yaml.safe_load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON file: {e}")
        except Exception as e:
            if YAML_AVAILABLE and format_type == 'yaml':
                raise ValueError(f"Invalid YAML file: {e}")
            else:
                raise ValueError(f"Error loading file: {e}")
    
    def validate_data(self, data: Dict[str, Any]) -> None:
        """
        Validate data against schema.
        
        Args:
            data: Data to validate
            
        Raises:
            jsonschema.ValidationError: If validation fails
        """
        try:
            jsonschema.validate(instance=data, schema=self.schema)
        except jsonschema.ValidationError:
            raise  # Re-raise with original error message
    
    def load_and_validate(self, filepath: str) -> Dict[str, Any]:
        """
        Load and validate data from file.
        
        Args:
            filepath: Path to the data file
            
        Returns:
            Validated data dictionary
            
        Raises:
            Various exceptions for file/validation errors
        """
        data = self.load_data(filepath)
        self.validate_data(data)
        return data
    
    def save_data(self, data: Dict[str, Any], filepath: str, 
                  format_type: Optional[Literal['json', 'yaml']] = None,
                  pretty: bool = True) -> None:
        """
        Save data to JSON or YAML file.
        
        Args:
            data: Data to save
            filepath: Output file path
            format_type: 'json' or 'yaml'. If None, detected from filepath
            pretty: Whether to format output nicely
        """
        if format_type is None:
            format_type = self.detect_format(filepath)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            if format_type == 'json':
                if pretty:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                else:
                    json.dump(data, f, ensure_ascii=False)
            else:  # yaml
                if not YAML_AVAILABLE:
                    raise ImportError("PyYAML is required for YAML file support. Install with: pip install PyYAML")
                yaml.dump(data, f, default_flow_style=False, 
                         allow_unicode=True, sort_keys=False)
