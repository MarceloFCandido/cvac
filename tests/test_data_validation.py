import pytest
import json
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from cvac.cv_to_docx import CVData

@pytest.fixture
def valid_cv_data():
    return {
        "personalInfo": {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "location": {
                "city": "New York"
            }
        },
        "workExperience": [],
        "education": []
    }

@pytest.fixture
def invalid_cv_data():
    return {
        "personalInfo": {
            "firstName": "Jane",
            "lastName": "Doe"
        },
        "workExperience": [],
        "education": []
    }

@pytest.fixture
def create_test_files(tmp_path, valid_cv_data, invalid_cv_data):
    # Create schema file
    schema_content = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "CV Schema",
        "type": "object",
        "required": ["personalInfo", "workExperience", "education"],
        "properties": {
            "personalInfo": {
                "type": "object",
                "required": ["firstName", "lastName", "email"],
                 "properties": {
                    "firstName": {"type": "string"},
                    "lastName": {"type": "string"},
                    "email": {"type": "string", "format": "email"}
                }
            },
            "workExperience": {"type": "array"},
            "education": {"type": "array"}
        }
    }
    schema_file = tmp_path / "schema.json"
    schema_file.write_text(json.dumps(schema_content))

    # Create valid CV file
    valid_cv_file = tmp_path / "valid_cv.json"
    valid_cv_file.write_text(json.dumps(valid_cv_data))

    # Create invalid CV file
    invalid_cv_file = tmp_path / "invalid_cv.json"
    invalid_cv_file.write_text(json.dumps(invalid_cv_data))

    return schema_file, valid_cv_file, invalid_cv_file

def test_valid_cv_data_loads_successfully(create_test_files):
    schema_file, valid_cv_file, _ = create_test_files
    cv_data = CVData(str(valid_cv_file), str(schema_file))
    assert cv_data.data is not None
    assert cv_data.data["personalInfo"]["firstName"] == "John"

def test_invalid_cv_data_raises_error(create_test_files):
    schema_file, _, invalid_cv_file = create_test_files
    with pytest.raises(SystemExit):
        CVData(str(invalid_cv_file), str(schema_file))

def test_missing_json_file_raises_error(tmp_path):
    schema_file = tmp_path / "schema.json"
    schema_file.write_text("{}")
    with pytest.raises(SystemExit):
        CVData("non_existent.json", str(schema_file))
