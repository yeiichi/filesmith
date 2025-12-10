"""
transfer.py — basic file copy/move operations for filesmith.

This module performs the minimal action layer:
- given a list of files
- and a destination directory

It copies or moves them with simple conflict policies.
"""

from __future__ import annotations
from pathlib import Path
from typing import Literal, Sequence
import shutil

TransferMode = Literal["copy", "move"]
OnConflict = Literal["skip", "overwrite", "error"]


def transfer_files(
    files: Sequence[Path],
    dest_root: Path,
    mode: TransferMode = "copy",
    on_conflict: OnConflict = "skip",
    dry_run: bool = False,
) -> list[tuple[Path, Path]]:
    """
    Copy or move `files` to `dest_root`.

    Parameters
    ----------
    files : Sequence[Path]
        Files to transfer.
    dest_root : Path
        Output directory (created if missing).
    mode : {"copy", "move"}
        Operation mode.
    on_conflict : {"skip", "overwrite", "error"}
        What to do when the destination file already exists.
    dry_run : bool
        If True, do not perform filesystem writes.

    Returns
    -------
    list[(Path, Path)]
        List of (source, destination) pairs.
    """

    dest_root = Path(dest_root).expanduser()
    dest_root.mkdir(parents=True, exist_ok=True)

    ops: list[tuple[Path, Path]] = []

    for src in files:
        dest = dest_root / src.name

        if dest.exists():
            if on_conflict == "skip":
                continue
            elif on_conflict == "error":
                raise FileExistsError(f"Destination exists: {dest}")
            # else overwrite

        ops.append((src, dest))

        if dry_run:
            continue

        if mode == "copy":
            shutil.copy2(src, dest)
        elif mode == "move":
            shutil.move(src, dest)
        else:
            raise ValueError(f"Invalid mode: {mode}")

    return ops
