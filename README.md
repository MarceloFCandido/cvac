# CVaC: CV-as-Code

Automate your CV/Resume generation from structured JSON or YAML data into a professional DOCX format with customizable styling.

## Overview

CVaC provides a robust solution for managing your Curriculum Vitae or Resume as structured JSON data. It leverages a Python script to transform this data into a well-formatted Microsoft Word (`.docx`) document, ensuring consistency and ease of updates.

## Features

- **JSON and YAML Support:** Define your CV content in either JSON or YAML format.
- **Bidirectional Conversion:** Convert between JSON and YAML formats seamlessly.
- **Schema Validation:** CV data is validated against a JSON schema to ensure correctness.
- **DOCX Output:** Generates professional `.docx` files compatible with standard word processors.
- **External Style Configuration:** Customize document styling via external JSON/YAML files.
- **Unified CLI:** Single command-line interface for all operations (generate, convert, validate).

## Usage

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/cvac.git
    cd cvac
    ```

2.  **Install Dependencies:**
    Ensure you have Python 3.8+ installed. Then, install the package:
    ```bash
    pip install -e .
    ```

### Command Line Interface

CVaC provides a unified CLI with multiple commands:

#### Generate CV Document

Generate a DOCX file from your CV data (JSON or YAML):

```bash
# Basic usage
cvac generate my_cv.yaml resume.docx

# With custom styling
cvac generate my_cv.json resume.docx --style custom_style.yaml

# Using the Python module directly
python -m src.cvac generate my_cv.yaml resume.docx
```

#### Convert Between Formats

Convert between JSON and YAML formats:

```bash
# JSON to YAML
cvac convert cv.json cv.yaml

# YAML to JSON
cvac convert cv.yaml cv.json --pretty
```

#### Validate CV Data

Validate your CV data against the schema:

```bash
cvac validate my_cv.yaml
```

### Prepare Your CV Data

Create your CV data in either JSON or YAML format following the structure defined in `schema/cv.schema.json`.

Example YAML format:
```yaml
personalInfo:
  firstName: John
  lastName: Doe
  email: john.doe@example.com
  location:
    city: San Francisco
    country: USA

workExperience:
  - company: Tech Corp
    position: Senior Developer
    startDate: "2020-01"
    current: true
    achievements:
      - Led team of 5 developers
      - Improved performance by 50%

education:
  - institution: University Name
    degree: Bachelor of Science
    field: Computer Science
    graduationDate: "2019-05"

skills:
  - Python
  - JavaScript
  - Docker
  # Skills can also be detailed objects:
  # - name: Python
  #   level: expert
  #   yearsOfExperience: 5

languages:
  - language: English
    native: true
  - language: Spanish
    proficiency: B2  # A1-C2 CEFR levels
```

### Custom Styling

Create a custom style file (JSON or YAML) to override default styling:

```json
{
  "font_name": "Arial",
  "font_size": 11,
  "name_font_size": 16,
  "margins": {
    "top": 20,
    "bottom": 20,
    "left": 25,
    "right": 25
  }
}
```

Then use it when generating:
```bash
cvac generate cv.yaml resume.docx --style my_style.json
```

### Backwards Compatibility

The original `cv_to_docx.py` script is maintained for backwards compatibility:
```bash
python cv_to_docx.py my_cv.json output_resume.docx
```

### As a Git Submodule

You can integrate CVaC into another Git repository as a submodule, which is useful for managing your CV data and generation workflow within a larger project (e.g., a personal website repository).

1.  **Add CVaC as a submodule:**
    Navigate to your main repository and add CVaC:
    ```bash
    git submodule add https://github.com/MarceloFCandido/cvac.git cvac
    git submodule update --init --recursive
    ```
    (Replace `https://github.com/MarceloFCandido/cvac.git` with the appropriate URL if you've forked the repository.)

2.  **Structure your main repository:**
    Place your `cv.json` data file in a location accessible to the submodule, for example, in a `data/` directory at the root of your main repository.

3.  **Automate with GitHub Actions (Example):**
    You can set up a GitHub Actions workflow in your main repository to automatically generate your CV when `cv.json` is updated. Here's an example `generate-resume.yml`:

    ```yaml
    name: Generate and Release Resume

    on:
      push:
        branches:
          - master
        paths:
          - 'data/cv.json' # Path to your CV data in the main repo
      workflow_dispatch:

    permissions:
      contents: write

    jobs:
      build:
        runs-on: ubuntu-latest
        
        steps:
          - name: Checkout code
            uses: actions/checkout@v4
            with:
              submodules: 'true' # Important: checkout submodules

          - name: Set up Python
            uses: actions/setup-python@v4
            with:
              python-version: '3.12'
          
          - name: Install dependencies
            run: |
              python -m pip install --upgrade pip
              pip install -r cvac/requirements.txt # Install dependencies from the submodule
          
          - name: Get current date
            id: date
            run: echo "DATE=$(date +'%Y-%m-%d')" >> $GITHUB_ENV
          
          - name: Get CV owner name
            id: cv-owner
            run: |
              OWNER_NAME=$(python -c "import json; print(json.load(open('data/cv.json'))['personalInfo']['firstName'] + ' ' + json.load(open('data/cv.json'))['personalInfo']['lastName'])")
              echo "OWNER_NAME=$OWNER_NAME" >> $GITHUB_ENV
          
          - name: Generate DOCX resume
            run: |
              python cvac/cvac.py generate data/cv.json resume.docx # Use the script from the submodule
          
          - name: Convert DOCX to PDF
            run: |
              sudo apt-get update
              sudo apt-get install -y libreoffice
              libreoffice --headless --convert-to pdf resume.docx
          
          - name: Create Release
            id: create_release
            uses: softprops/action-gh-release@v1
            with:
              tag_name: resume-${{ env.DATE }}
              name: ${{ env.OWNER_NAME }}'s Resume - ${{ env.DATE }}
              body: |
                Resume automatically generated on ${{ env.DATE }}
                
                This release was automatically created by the CI/CD pipeline.
              files: |
                resume.docx
                resume.pdf
              draft: false
            env:
              GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

          - name: Cleanup old releases
            uses: dev-drprasad/delete-older-releases@v0.2.0
            with:
              keep_latest: 5
            env:
              GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    ```
    This workflow checks out the main repository and its submodules, installs `cvac`'s dependencies, and then uses the `cv_to_docx.py` script from the submodule to generate the resume.


## JSON Schema (`schema/cv.schema.json`)

The `cv.schema.json` file defines the expected structure and types for your CV data. It ensures that your JSON input is valid before document generation. Refer to this file to understand the available fields for personal information, work experience, education, skills, languages, and more.

## Customizing Styles

CVaC now supports external style configuration files in JSON or YAML format. You can customize:

- Font family and sizes
- Document margins  
- Paragraph spacing
- Bullet point styling

See `examples/modern_style.json` and `examples/elegant_style.yaml` for examples.

## Project Structure

```
cvac/
├── .gitignore
├── pyproject.toml
├── README.md
├── schema/
│   └── cv.schema.json          # JSON schema for CV data validation
├── src/
│   ├── __init__.py
│   ├── cvac.py                 # Main CLI entry point
│   ├── cv_to_docx.py           # Legacy script (backwards compatibility)
│   ├── style.py                # Default styling configuration
│   ├── commands/               # CLI command implementations
│   │   ├── __init__.py
│   │   ├── convert.py          # Format conversion command
│   │   ├── generate.py         # Document generation command
│   │   └── validate.py         # Data validation command
│   └── core/                   # Core functionality
│       ├── __init__.py
│       ├── data_handler.py     # JSON/YAML data handling
│       └── style_loader.py     # Style configuration loading
├── tests/
│   ├── test_converter.py       # Conversion tests
│   ├── test_data_handler.py    # Data handling tests
│   ├── test_data_validation.py # Legacy validation tests
│   ├── test_document_generation.py # Document generation tests
│   └── test_style_loader.py    # Style loading tests
└── examples/
    ├── sample_cv.yaml          # Example CV in YAML format
    ├── comprehensive_cv.yaml   # Example using ALL schema fields
    ├── cv_with_detailed_skills.json  # Example with mixed skill formats
    ├── modern_style.json       # Modern style configuration
    └── elegant_style.yaml      # Elegant style configuration
```

## Dependencies

-   `python-docx`: For creating and modifying Word documents.
-   `jsonschema`: For validating data against the schema.
-   `PyYAML`: For YAML file support.

These are managed via `pyproject.toml`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
