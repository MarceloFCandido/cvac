#!/usr/bin/env python3
"""
CVaC - CV as Code
Main CLI entry point for all CV operations.
"""

import argparse
import sys
import os
from pathlib import Path

from .commands.generate import generate_command
from .commands.convert import convert_command
from .commands.validate import validate_command


def main():
    parser = argparse.ArgumentParser(
        description='CVaC: CV-as-Code - Generate professional CVs from structured data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s generate cv.yaml resume.docx
  %(prog)s generate cv.json resume.docx --style modern.json
  %(prog)s convert cv.json cv.yaml
  %(prog)s validate cv.yaml
        """
    )
    
    parser.add_argument('--version', action='version', version='CVaC 1.2.0')
    
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands',
        metavar='COMMAND'
    )
    
    # Generate subcommand (the main feature)
    generate_parser = subparsers.add_parser(
        'generate',
        help='Generate DOCX document from CV data',
        description='Generate a professional DOCX document from JSON/YAML CV data'
    )
    generate_parser.add_argument(
        'input',
        help='Input CV file (JSON or YAML format)'
    )
    generate_parser.add_argument(
        'output',
        nargs='?',
        default='resume-generated.docx',
        help='Output DOCX file (default: resume-generated.docx)'
    )
    generate_parser.add_argument(
        '--style', '-s',
        help='Custom style configuration file (JSON or YAML)'
    )
    
    # Convert subcommand
    convert_parser = subparsers.add_parser(
        'convert',
        help='Convert between JSON and YAML formats',
        description='Convert CV data between JSON and YAML formats'
    )
    convert_parser.add_argument(
        'input',
        help='Input file (JSON or YAML)'
    )
    convert_parser.add_argument(
        'output',
        help='Output file (format detected from extension)'
    )
    convert_parser.add_argument(
        '--pretty', '-p',
        action='store_true',
        help='Pretty print output with proper formatting'
    )
    
    # Validate subcommand
    validate_parser = subparsers.add_parser(
        'validate',
        help='Validate CV data against schema',
        description='Validate CV data file against the JSON schema'
    )
    validate_parser.add_argument(
        'input',
        help='CV data file to validate (JSON or YAML)'
    )
    validate_parser.add_argument(
        '--schema',
        help='Custom schema file (default: built-in CV schema)'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle commands
    if args.command == 'generate':
        return generate_command(args)
    elif args.command == 'convert':
        return convert_command(args)
    elif args.command == 'validate':
        return validate_command(args)
    else:
        # If no command specified, show help
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
