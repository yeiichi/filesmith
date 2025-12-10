"""
DOCX-specific XML helpers (minimal stub).

This module exposes:
    - namespace constants for WordprocessingML
    - small helpers for checking node types

These are intentionally tiny to avoid overcommitting the API
while allowing clean future expansion.
"""

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def is_text_node(node) -> bool:
    """Return True if the XML Element is a w:t node."""
    return node.tag == W_NS + "t"


def is_paragraph(node) -> bool:
    """Return True if the Element is a w:p node."""
    return node.tag == W_NS + "p"
