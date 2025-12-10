# tests/test_simple_pptx_editor.py

from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

import pytest

from ooxlm.pptx import SimplePptxEditor

SLIDE1_XML = b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
       xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:sp>
        <p:txBody>
          <a:p>
            <a:r><a:t>Hello</a:t></a:r>
            <a:r><a:t> world</a:t></a:r>
          </a:p>
        </p:txBody>
      </p:sp>
    </p:spTree>
  </p:cSld>
</p:sld>
"""

SLIDE2_XML = b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
       xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:sp>
        <p:txBody>
          <a:p>
            <a:r><a:t>Second</a:t></a:r>
            <a:r><a:t> slide</a:t></a:r>
          </a:p>
        </p:txBody>
      </p:sp>
    </p:spTree>
  </p:cSld>
</p:sld>
"""


def create_minimal_pptx(path: Path) -> None:
    """
    Create a minimal PPTX-like ZIP with two slide XML files.

    This is not a valid PowerPoint file (no relationships, content types),
    but it is sufficient for SimplePptxEditor, which only relies on the
    presence and contents of ppt/slides/slide*.xml.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(path, "w") as zf:
        zf.writestr("ppt/slides/slide1.xml", SLIDE1_XML)
        zf.writestr("ppt/slides/slide2.xml", SLIDE2_XML)


def test_get_text_concatenates_text_across_slides(tmp_path: Path) -> None:
    pptx_path = tmp_path / "test.pptx"
    create_minimal_pptx(pptx_path)

    editor = SimplePptxEditor(pptx_path)
    text = editor.get_text(separator=" ")

    # Slide1: "Hello" " world" -> "Hello  world" with naive join by " "
    # Slide2: "Second" " slide"
    # Combined naive sequence: ["Hello", " world", "Second", " slide"]
    assert text == "Hello  world Second  slide"


def test_replace_updates_text_and_save_writes_new_pptx(tmp_path: Path) -> None:
    src_path = tmp_path / "src.pptx"
    out_path = tmp_path / "out.pptx"
    create_minimal_pptx(src_path)

    editor = SimplePptxEditor(src_path)
    changed_nodes = editor.replace("world", "PPTX")
    assert changed_nodes == 1

    editor.save(out_path)
    assert out_path.is_file()

    # Reload the saved presentation and verify text was updated
    editor2 = SimplePptxEditor(out_path)
    text = editor2.get_text(separator=" ")
    assert "PPTX" in text
    assert "world" not in text


def test_init_raises_on_missing_file(tmp_path: Path) -> None:
    missing = tmp_path / "does_not_exist.pptx"
    with pytest.raises(FileNotFoundError):
        SimplePptxEditor(missing)


def test_init_raises_on_no_slides(tmp_path: Path) -> None:
    # Create an empty ZIP with no ppt/slides/slide*.xml
    path = tmp_path / "broken.pptx"
    with ZipFile(path, "w") as zf:
        zf.writestr("[Content_Types].xml", "<Types></Types>")

    with pytest.raises(RuntimeError):
        SimplePptxEditor(path)
