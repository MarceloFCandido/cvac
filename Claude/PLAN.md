### Plan to Implement Full CV Schema Rendering in DOCX

This plan outlines the necessary steps to extend the `DocxGenerator` class in `src/cvac/cv_to_docx.py` to render all fields defined in `schema/cv.schema.json`.

**Objective:** Achieve 100% coverage of the CV schema in the generated DOCX output.

**Primary File to Modify:** `src/cvac/cv_to_docx.py`

**Important Notes:**
- All new sections and fields are **optional** - the document should generate successfully even if these fields are not present in the CV data
- The `metadata` field from the schema should **NOT** be rendered in the document as it's for internal version control only
- Each section method should check if its data exists before rendering

---

### **Step 1: Implement the `summary` Section**

This section should appear right after the personal contact information.

1.  **Create a new method:** `_create_summary_section(self)`.
2.  **Logic:**
    *   Check if `self.cv_data.data.get("summary")` exists.
    *   If it does, add a section header titled "SUMMARY" or "PROFESSIONAL SUMMARY".
    *   Add a new paragraph with the content of the `summary` field.
3.  **Integration:** Call `self._create_summary_section()` from the main `generate()` method, after `_create_personal_info_section()`.

### **Step 2: Enhance the `workExperience` and `education` Sections**

These sections are partially implemented. The goal is to add the missing fields.

1.  **Modify `_create_experience_section(self)`:**
    *   **Location:** After the company name or position, add the job's `location`.
    *   **Technologies:** After the description and achievements, add a line like "Technologies used: " followed by a comma-separated list from the `technologies` array.
2.  **Modify `_create_education_section(self)`:**
    *   **GPA:** If `gpa` exists, add it next to the degree or on a new line (e.g., "GPA: 3.8/4.0").
    *   **Description/Achievements:** If `description` or `achievements` exist, add them as bullet points under the respective education entry, similar to how work experience achievements are handled.

### **Step 3: Implement the `projects` Section**

This is a completely new section.

1.  **Create a new method:** `_create_projects_section(self)`.
2.  **Logic:**
    *   Check for the `projects` array in the data.
    *   Add a section header: "PROJECTS".
    *   Iterate through each project and render the following:
        *   **Project Name:** In bold, followed by a hyperlink if `url` is present.
        *   **Dates:** Formatted `startDate` - `endDate`.
        *   **Repository:** A hyperlink to the `repositoryUrl` if available.
        *   **Description:** As a standard paragraph.
        *   **Technologies:** As a list of bullet points or a comma-separated list.
3.  **Integration:** Call `self._create_projects_section()` in `generate()`, logically placing it after the experience section.

### **Step 4: Implement the `certifications` Section**

This is a new section, typically placed after education.

1.  **Create a new method:** `_create_certifications_section(self)`.
2.  **Logic:**
    *   Check for the `certifications` array.
    *   Add a section header: "CERTIFICATIONS".
    *   For each certification, create a paragraph containing:
        *   `name` (bold), `issuer`, and `issueDate`.
        *   Include a hyperlink if `url` is available.
        *   Example: **Certified Kubernetes Administrator**, The Linux Foundation, Issued Oct 2023
3.  **Integration:** Call `self._create_certifications_section()` in `generate()`, after the education section.

### **Step 5: Implement the `publications` Section**

A new section for academic or professional publications.

1.  **Create a new method:** `_create_publications_section(self)`.
2.  **Logic:**
    *   Check for the `publications` array.
    *   Add a section header: "PUBLICATIONS".
    *   For each publication, render its details, including `title` (bold), `authors`, `publisher`, and `publicationDate`. Add a hyperlink for `url` or `doi`.
4.  **Integration:** Call `self._create_publications_section()` in `generate()`.

### **Step 6: Enhance the `skills` Section**

The current implementation just lists skill names. It should be enhanced to show categories and levels.

1.  **Modify `_create_skills_section(self)`:**
    *   Instead of a single comma-separated paragraph, group skills by `category`.
    *   For each category, add a sub-heading (e.g., "Programming Languages:", "Databases:", "Cloud Platforms:").
    *   Under each sub-heading, list the skills. If a skill has a `level` (e.g., "expert", "proficient"), you could append it in parentheses.
    *   **Make the section header configurable**: If skills have categories, use "SKILLS"; otherwise, keep "TECHNOLOGIES" or make it style-configurable.

### **Step 7: Implement `references` and `customSections`**

1.  **References:**
    *   Create a `_create_references_section(self)` method.
    *   Check for the `references` array.
    *   Typically, CVs don't list full contact details for references. The best practice is to add a single line: "References available upon request." This should be the default behavior unless the schema data is explicitly populated.
2.  **Custom Sections:**
    *   Create a `_create_custom_sections(self)` method.
    *   Check for the `customSections` array.
    *   Iterate through it. For each item, use its `title` as a new section header and its `content` as the paragraph text.

### **Step 8: Additional Implementation Considerations**

1. **Date Format Flexibility:**
   - The existing `_format_date()` method handles "YYYY-MM" format
   - Some sections (certifications, publications) might use different formats (e.g., "YYYY" only)
   - Consider enhancing `_format_date()` to handle multiple date formats:
     - "YYYY-MM-DD" → "January 15, 2025"
     - "YYYY-MM" → "January 2025"
     - "YYYY" → "2025"

2. **Configurable Section Ordering:**
   - Add a `section_order` field to the style configuration
   - Allow users to customize the order of sections in their CV
   - Default order if not specified: personalInfo → summary → workExperience → education → projects → skills → certifications → publications → awards → volunteerWork → languages → references → customSections
   - Implementation: Create a mapping of section names to their render methods and iterate based on the configured order

3. **Error Handling:**
   - Each section method should gracefully handle missing or malformed data
   - Use try-except blocks where appropriate, especially for date parsing and URL formatting
   - Log warnings for malformed data but continue document generation

### **Step 9: Create a Comprehensive Test File**

To verify the implementation, create a new YAML file, `examples/comprehensive_cv.yaml`, that includes every single field from the `cv.schema.json` (except `metadata`). This will serve as the master test case for ensuring all data is rendered correctly.

By following this plan, all fields in the CV schema will be correctly rendered in the final DOCX document, making the tool feature-complete.
