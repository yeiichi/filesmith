# src/ooxlm/common/zip_ops.py

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping
from zipfile import ZipFile, ZIP_DEFLATED

PathLike = str | Path
BytesMapping = Mapping[str, bytes]


def list_members(zip_path: PathLike) -> list[str]:
    """
    Return a list of all member names inside the ZIP archive.

    Parameters
    ----------
    zip_path : str | Path
        Path to the .zip/.docx/.pptx file.

    Returns
    -------
    list[str]
        List of member paths (e.g. "word/document.xml").
    """
    zip_path = Path(zip_path)
    with ZipFile(zip_path) as zf:
        return zf.namelist()


def load_member(zip_path: PathLike, member: str) -> bytes:
    """
    Load a single member from the ZIP archive as raw bytes.

    Parameters
    ----------
    zip_path : str | Path
        Path to the .zip/.docx/.pptx file.
    member : str
        Internal path inside the archive (e.g. "word/document.xml").

    Returns
    -------
    bytes
        Raw contents of the member.

    Raises
    ------
    KeyError
        If the member does not exist.
    """
    zip_path = Path(zip_path)
    with ZipFile(zip_path) as zf:
        return zf.read(member)


def load_members(zip_path: PathLike, members: Iterable[str]) -> dict[str, bytes]:
    """
    Load multiple members from the ZIP archive.

    Parameters
    ----------
    zip_path : str | Path
        Path to the .zip/.docx/.pptx file.
    members : Iterable[str]
        Internal paths inside the archive.

    Returns
    -------
    dict[str, bytes]
        Mapping {member_name: content_bytes}.

    Notes
    -----
    This will raise KeyError if any member is missing.
    """
    zip_path = Path(zip_path)
    result: dict[str, bytes] = {}
    with ZipFile(zip_path) as zf:
        for name in members:
            result[name] = zf.read(name)
    return result


def load_all(zip_path: PathLike) -> dict[str, bytes]:
    """
    Load all members from the ZIP archive into memory.

    Parameters
    ----------
    zip_path : str | Path
        Path to the .zip/.docx/.pptx file.

    Returns
    -------
    dict[str, bytes]
        Mapping {member_name: content_bytes}.
    """
    zip_path = Path(zip_path)
    result: dict[str, bytes] = {}
    with ZipFile(zip_path) as zf:
        for info in zf.infolist():
            result[info.filename] = zf.read(info.filename)
    return result


def rewrite_zip(
    zip_path: PathLike,
    output_path: PathLike,
    *,
    replacements: BytesMapping,
    drop: Iterable[str] | None = None,
) -> None:
    """
    Rebuild a ZIP archive with some members replaced and/or dropped.

    This is the core primitive used by the OOXML editors:
    - Read original DOCX/PPTX
    - Replace e.g. "word/document.xml" with modified XML bytes
    - Write out a new OOXML file

    Parameters
    ----------
    zip_path : str | Path
        Path to the source .zip/.docx/.pptx file.
    output_path : str | Path
        Path to the destination file.
    replacements : Mapping[str, bytes]
        Mapping of {member_name: new_content_bytes}.
        If a key exists in the original archive, its content is replaced.
        If a key does NOT exist in the original, it will be ADDED as a new file.
    drop : Iterable[str] | None, optional
        Iterable of member names to omit from the output archive.

    Notes
    -----
    - File metadata (dates, permissions, compression type) is preserved
      for existing members by reusing the original ZipInfo objects.
    - New members (not present in the original) are written with
      default metadata and ZIP_DEFLATED compression.
    """
    src = Path(zip_path)
    dst = Path(output_path)

    to_drop = set(drop or [])

    with ZipFile(src) as zin, ZipFile(dst, "w", compression=ZIP_DEFLATED) as zout:
        handled: set[str] = set()

        # Copy existing members, applying replacements/drops
        for info in zin.infolist():
            name = info.filename

            if name in to_drop:
                # Skip this member entirely
                continue

            if name in replacements:
                data = replacements[name]
                handled.add(name)
            else:
                data = zin.read(name)

            # Preserve original metadata (ZipInfo) where possible
            zout.writestr(info, data)

        # Add any replacement entries that did not exist in original
        for name, data in replacements.items():
            if name in handled:
                continue
            # New member with default metadata
            zout.writestr(name, data)


def copy_zip(src: PathLike, dst: PathLike) -> None:
    """
    Make a simple copy of a ZIP archive.

    This is essentially:

        rewrite_zip(src, dst, replacements={}, drop=None)

    but implemented directly to avoid extra dict/set overhead.

    Parameters
    ----------
    src : str | Path
        Source path.
    dst : str | Path
        Destination path.
    """
    src = Path(src)
    dst = Path(dst)

    with ZipFile(src) as zin, ZipFile(dst, "w", compression=ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            zout.writestr(info, data)
