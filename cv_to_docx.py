#!/usr/bin/env python3
"""
Backwards compatibility wrapper for cv_to_docx.py
"""

import sys
from src.cvac.cv_to_docx import main

if __name__ == "__main__":
    sys.exit(main())
