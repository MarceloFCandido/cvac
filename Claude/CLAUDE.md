
# Claude Development Guide

This document provides essential context about the CVaC repository to help you understand its structure, architecture, and purpose. Use this as a quick reference guide for development and debugging tasks.

For a user-facing overview, please see `README.md`.

## 1. Core Purpose

CVaC (CV-as-Code) is a Python-based command-line tool designed to **generate professional `.docx` resumes from structured YAML or JSON data**. It allows users to maintain their resume content in a version-controllable format and automate the creation of polished documents with customizable styling.

## 2. Tech Stack

- **Language:** Python 3
- **Primary Libraries:**
    - `python-docx`: For creating and manipulating Microsoft Word (`.docx`) files.
    - `jsonschema`: For validating input data against the defined CV schema.
    - `PyYAML`: For reading and writing YAML files.
- **CLI Framework:** The standard `argparse` library is used for parsing command-line arguments.
- **Testing:** `pytest` is the framework used for all tests.
- **Packaging:** `setuptools` is used for packaging and distribution, configured in `pyproject.toml`.

## 3. Architectural Principles

The project follows a clean, modular, and testable architecture based on the principle of **separation of concerns**.

- **CLI Entry Point (`src/cvac/__main__.py`):** This is the single entry point for the `cvac` command. Its only job is to parse arguments and delegate to the appropriate command handler.

- **Command-Oriented Structure (`src/cvac/commands/`):**
    - Each subcommand (`generate`, `convert`, `validate`) has its own dedicated module in this directory.
    - This keeps the logic for each action isolated and easy to maintain.

- **Core Logic Abstraction (`src/cvac/core/`):**
    - This directory contains the reusable, high-level business logic, decoupled from the CLI.
    - **`DataHandler`**: A crucial class that centralizes all data operations: loading JSON/YAML, detecting file formats, and **validating data against the schema**. Any operation involving reading or writing data should use this handler.
    - **`StyleLoader`**: This class manages all styling concerns. It loads the default style, merges it with any user-provided custom style file, validates the result, and prepares it for the document generator.

- **Schema-Driven Data Model (`schema/cv.schema.json`):**
    - The structure of the CV is not arbitrary; it is strictly defined by this JSON schema.
    - The `DataHandler` uses this schema as the **single source of truth** for data validation, ensuring data integrity before any document generation occurs.

- **Rendering Engine (`src/cvac/cv_to_docx.py`):**
    - The `DocxGenerator` class is the heart of the document creation process.
    - It is intentionally kept separate from data loading and CLI logic. Its sole responsibility is to take validated data and a style configuration and render the `.docx` file.
    - **To add or modify how CV sections are rendered, this is the primary file to edit.**

## 4. Key Workflow: `cvac generate`

Understanding the `generate` command's workflow is key to understanding the whole application:

1.  **CLI Parsing:** `__main__.py` receives the `generate` command and its arguments (`input`, `output`, `style`).
2.  **Command Handling:** It calls `generate_command()` in `src/cvac/commands/generate.py`.
3.  **Data Loading:** `generate_command` instantiates `DataHandler` and calls `load_and_validate()` on the input file. This returns a validated Python dictionary of the CV data.
4.  **Style Loading:** It then instantiates `StyleLoader` and calls `load_style()`, passing the path to the custom style file if provided. This returns a merged and validated style dictionary.
5.  **Document Generation:** It creates an instance of `DocxGenerator`, passing the CV data and style configuration to its constructor.
6.  **File Saving:** Finally, it calls the `generator.generate(output_path)` method, which builds the document section by section and saves the final `.docx` file.

## 5. Debugging and Development Tips

- **Start with the Schema:** Before implementing a new field, always check its definition in `schema/cv.schema.json` to understand its type and structure.
- **Look at the Tests:** The `tests/` directory contains valuable examples of how each component is expected to function in isolation.
- **Use the `validate` command:** Before debugging a generation issue, run `cvac validate your_cv.yaml` to ensure the input data is not the source of the problem.
- **Isolate Concerns:** When adding a feature, think about where the logic belongs. Is it a core data operation (`DataHandler`), a styling feature (`StyleLoader`), a rendering task (`DocxGenerator`), or a new CLI command (`commands/`)?
