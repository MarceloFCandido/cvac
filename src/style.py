from docx.shared import Pt, Cm, Mm

STYLE_CONFIG = {
    "font_name": "Calibri",
    "font_size": 11,
    "name_font_size": 14,
    "heading_font_size": 11,
    "margins": {
        "top": Mm(15),
        "bottom": Mm(15),
        "left": Mm(15),
        "right": Mm(15),
    },
    "paragraph_spacing": {
        "before": 0,
        "after": 2,
        "line_spacing": 1,
    },
    "bullet_style": {
        "left_indent": Cm(0.5),
        "first_line_indent": Cm(-0.25),
        "line_spacing": 1.0,
        "space_after": Pt(3),
        "space_before": Pt(0),
    },
}
