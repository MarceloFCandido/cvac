"""
Generate command - creates DOCX from CV data.
"""

import sys
import os
from pathlib import Path

from ..core.data_handler import DataHandler
from ..core.style_loader import StyleLoader
from ..cv_to_docx import DocxGenerator


def generate_command(args):
    """
    Handle the generate command.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        0 on success, 1 on error
    """
    try:
        print(f"Loading CV data from {args.input}...")
        
        # Load and validate CV data
        data_handler = DataHandler()
        cv_data = data_handler.load_and_validate(args.input)
        
        # Load style configuration
        style_loader = StyleLoader()
        if args.style:
            print(f"Loading custom style from {args.style}...")
        style_config = style_loader.load_style(args.style)
        
        # Create a simple object to hold the data (to match existing DocxGenerator interface)
        class CVDataWrapper:
            def __init__(self, data):
                self.data = data
        
        cv_wrapper = CVDataWrapper(cv_data)
        
        # Generate the document
        print(f"Generating document...")
        generator = DocxGenerator(cv_wrapper, style_config)
        generator.generate(args.output)
        
        print(f"✅ Successfully generated {args.output}")
        return 0
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        if hasattr(e, '__traceback__'):
            import traceback
            traceback.print_exc()
        return 1
