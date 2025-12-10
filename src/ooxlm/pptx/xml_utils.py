"""
PPTX-specific XML helpers (minimal stub).

Provides:
    - namespace constants for DrawingML
    - small helpers for checking text nodes
"""

A_NS = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


def is_text_node(node) -> bool:
    """Return True if the XML Element is an a:t node."""
    return node.tag == A_NS + "t"
