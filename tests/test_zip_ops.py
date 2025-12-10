# tests/test_zip_ops.py

from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

from ooxlm.common.zip_ops import (
    list_members,
    load_member,
    rewrite_zip,
)


def _create_sample_zip(path: Path) -> None:
    """
    Create a simple ZIP file with three text members.

    Members:
      - "a.txt" -> b"A"
      - "b.txt" -> b"B"
      - "c.txt" -> b"C"
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(path, "w") as zf:
        zf.writestr("a.txt", b"A")
        zf.writestr("b.txt", b"B")
        zf.writestr("c.txt", b"C")


def test_rewrite_zip_replaces_drops_and_adds(tmp_path: Path) -> None:
    src = tmp_path / "src.zip"
    dst = tmp_path / "dst.zip"
    _create_sample_zip(src)

    # Sanity check: original members
    original_members = set(list_members(src))
    assert original_members == {"a.txt", "b.txt", "c.txt"}

    # Rewrite:
    # - Replace "b.txt" with "B2"
    # - Drop "c.txt"
    # - Add "new.txt"
    rewrite_zip(
        src,
        dst,
        replacements={
            "b.txt": b"B2",
            "new.txt": b"NEW",
        },
        drop=["c.txt"],
    )

    assert dst.is_file()

    members = set(list_members(dst))
    assert members == {"a.txt", "b.txt", "new.txt"}

    # Check contents
    assert load_member(dst, "a.txt") == b"A"
    assert load_member(dst, "b.txt") == b"B2"
    assert load_member(dst, "new.txt") == b"NEW"
