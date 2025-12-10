"""
finder.py — minimal file-finding utilities for filesmith.

This module provides the basic `find_files()` function,
intended to serve as the foundation for higher-level "find & move"
operations inside the package.

Future extensions may include:
- size filters
- modified-before/after
- suffix filters
- ignoring certain directories
"""

from __future__ import annotations
from pathlib import Path
from typing import Callable, Iterable, Optional

PathPredicate = Callable[[Path], bool]


def find_files(
    root: Path,
    pattern: str = "*",
    recursive: bool = True,
    predicate: Optional[PathPredicate] = None,
) -> list[Path]:
    """
    Find files under `root` using glob or rglob and optional filtering.

    Parameters
    ----------
    root : Path
        Base directory to search.
    pattern : str
        Glob pattern, e.g. "*.txt".
    recursive : bool
        If True, use rglob; else glob.
    predicate : Callable[[Path], bool], optional
        Optional per-file test. If provided, keep only files where predicate(file) is True.

    Returns
    -------
    list[Path]
        Matching files.
    """

    root = Path(root).expanduser()

    iterator: Iterable[Path]
    iterator = root.rglob(pattern) if recursive else root.glob(pattern)

    results: list[Path] = []
    for p in iterator:
        if not p.is_file():
            continue
        if predicate and not predicate(p):
            continue
        results.append(p)

    return results
