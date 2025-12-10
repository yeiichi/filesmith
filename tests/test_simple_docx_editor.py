# tests/test_simple_docx_editor.py

from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

import pytest

from ooxlm.docx import SimpleDocxEditor

DOCUMENT_XML_CONTENT = b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:p><w:r><w:t>Hello</w:t></w:r></w:p>
    <w:p><w:r><w:t> world</w:t></w:r></w:p>
  </w:body>
</w:document>
"""


def create_minimal_docx(path: Path, document_xml: bytes = DOCUMENT_XML_CONTENT) -> None:
    """
    Create a minimal DOCX file containing only word/document.xml.

    This is sufficient for SimpleDocxEditor, which only relies on
    the existence and contents of that file inside the ZIP archive.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(path, "w") as zf:
        zf.writestr("word/document.xml", document_xml)


def test_get_text_concatenates_text_nodes(tmp_path: Path) -> None:
    docx_path = tmp_path / "hello_world.docx"
    create_minimal_docx(docx_path)

    editor = SimpleDocxEditor(docx_path)
    text = editor.get_text()

    # Our sample document has "Hello" and " world" in separate w:t nodes
    assert text == "Hello world"


def test_replace_updates_text_and_save_writes_new_docx(tmp_path: Path) -> None:
    src_path = tmp_path / "src.docx"
    out_path = tmp_path / "out.docx"
    create_minimal_docx(src_path)

    editor = SimpleDocxEditor(src_path)

    changed_nodes = editor.replace("world", "DOCX")
    assert changed_nodes == 1

    editor.save(out_path)
    assert out_path.is_file()

    # Reload the saved document and verify text was updated
    editor2 = SimpleDocxEditor(out_path)
    text = editor2.get_text()
    assert text == "Hello DOCX"


def test_init_raises_on_missing_file(tmp_path: Path) -> None:
    missing = tmp_path / "does_not_exist.docx"
    with pytest.raises(FileNotFoundError):
        SimpleDocxEditor(missing)


def test_init_raises_on_missing_document_xml(tmp_path: Path) -> None:
    # Create an empty ZIP without word/document.xml
    path = tmp_path / "broken.docx"
    with ZipFile(path, "w") as zf:
        zf.writestr("[Content_Types].xml", "<Types></Types>")

    with pytest.raises(RuntimeError):
        SimpleDocxEditor(path)
