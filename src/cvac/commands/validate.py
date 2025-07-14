"""
Validate command - validates CV data against schema.
"""

import sys
import os
from pathlib import Path
import jsonschema

from ..core.data_handler import DataHandler


def validate_command(args):
    """
    Handle the validate command.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        0 on success, 1 on error
    """
    try:
        print(f"Validating {args.input}...")
        
        # Create data handler with custom schema if provided
        data_handler = DataHandler(schema_path=args.schema)
        
        # Load and validate
        data = data_handler.load_and_validate(args.input)
        
        # If we get here, validation passed
        print(f"✅ Validation successful!")
        print(f"   File format: {data_handler.detect_format(args.input).upper()}")
        
        # Show some basic stats about the CV
        if 'personalInfo' in data:
            name_parts = []
            for key in ['firstName', 'middleName', 'lastName']:
                if key in data['personalInfo'] and data['personalInfo'][key]:
                    name_parts.append(data['personalInfo'][key])
            if name_parts:
                print(f"   Name: {' '.join(name_parts)}")
        
        if 'workExperience' in data:
            print(f"   Work experiences: {len(data['workExperience'])}")
        
        if 'education' in data:
            print(f"   Education entries: {len(data['education'])}")
        
        if 'skills' in data:
            print(f"   Skills listed: {len(data['skills'])}")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return 1
    except jsonschema.ValidationError as e:
        print(f"❌ Validation failed!")
        print(f"   Error: {e.message}")
        if e.absolute_path:
            print(f"   Path: {' -> '.join(str(p) for p in e.absolute_path)}")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
