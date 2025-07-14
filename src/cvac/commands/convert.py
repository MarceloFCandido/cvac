"""
Convert command - converts between JSON and YAML formats.
"""

import sys
import os
from pathlib import Path

from ..core.data_handler import DataHandler


def convert_command(args):
    """
    Handle the convert command.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        0 on success, 1 on error
    """
    try:
        # Validate input and output are different
        if args.input == args.output:
            print("❌ Error: Input and output files must be different")
            return 1
        
        print(f"Loading data from {args.input}...")
        
        # Load data (with validation)
        data_handler = DataHandler()
        data = data_handler.load_and_validate(args.input)
        
        # Detect output format from extension
        output_format = data_handler.detect_format(args.output)
        
        print(f"Converting to {output_format.upper()} format...")
        
        # Save in the new format
        data_handler.save_data(data, args.output, format_type=output_format, pretty=args.pretty)
        
        print(f"✅ Successfully converted to {args.output}")
        return 0
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
