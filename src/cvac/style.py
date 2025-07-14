# Default style configuration for CVaC
# Values are in their base units (numbers) and will be converted to docx units when used

STYLE_CONFIG = {
    "font_name": "Calibri",
    "font_size": 11,
    "name_font_size": 14,
    "heading_font_size": 11,
    "margins": {
        "top": 15,      # millimeters
        "bottom": 15,   # millimeters
        "left": 15,     # millimeters
        "right": 15,    # millimeters
    },
    "paragraph_spacing": {
        "before": 0,
        "after": 2,
        "line_spacing": 1,
    },
    "bullet_style": {
        "left_indent": 0.5,        # centimeters
        "first_line_indent": -0.25, # centimeters
        "line_spacing": 1.0,
        "space_after": 3,          # points
        "space_before": 0,         # points
    },
}
