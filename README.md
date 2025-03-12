# Resume Automation

Automated CV/Resume generation using JSON data and GitHub Actions.

## Overview

This repository provides an infrastructure for maintaining your CV/resume as data in a JSON file, with automated generation of a formatted DOCX document on every update.

- Your CV data is stored in a JSON file (`data/cv.json`)
- The schema for the JSON data is defined in `schema/cv.schema.json`
- A Python script (`src/cv-to-docx.py`) converts the JSON data to a formatted DOCX file
- GitHub Actions automatically generates and releases the DOCX file when the JSON is updated

## How It Works

1. Update your CV data in `data/cv.json`
2. Commit and push the changes to the `main` branch
3. GitHub Actions automatically:
   - Detects changes to the CV data
   - Runs the Python script to generate a DOCX document
   - Creates a new GitHub release with the generated DOCX file

## Local Development

To generate the resume locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Generate the DOCX file
python src/cv-to-docx.py data/cv.json resume-generated.docx
```

## File Structure

- `.github/workflows/`: Contains GitHub Actions workflow definitions
- `src/`: Contains the Python script for generating the DOCX file
- `schema/`: Contains the JSON schema for validating CV data
- `data/`: Contains your CV data in JSON format

## Requirements

- Python 3.6+
- python-docx library

## License

MIT
