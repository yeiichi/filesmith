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
from typing import Callable, Iterator, Optional

PathPredicate = Callable[[Path], bool]


def find_files(
    root: Path | str,
    glob_pattern: str = "*",
    recursive: bool = True,
    predicate: Optional[PathPredicate] = None,
    *,
    pattern: str | None = None,
) -> Iterator[Path]:
    """
    Lazily find files under `root` using glob syntax and optional filtering.

    Parameters
    ----------
    root : Path | str
        Base directory to search.
    glob_pattern : str
        Glob pattern, e.g. ``*.txt``.
    recursive : bool
        If True, use ``Path.rglob()``; else ``Path.glob()``.
    predicate : Callable[[Path], bool], optional
        Optional per-file test. If provided, keep only files where predicate(file) is True.
    pattern : str, optional
        Deprecated compatibility alias for ``glob_pattern``.

    Returns
    -------
    Iterator[Path]
        Lazy iterator of matching files.
    """
    if pattern is not None:
        if glob_pattern != "*":
            raise ValueError("Use either glob_pattern or pattern, not both.")
        glob_pattern = pattern

    root = Path(root).expanduser()
    paths = root.rglob(glob_pattern) if recursive else root.glob(glob_pattern)

    for path in paths:
        if not path.is_file():
            continue
        if predicate and not predicate(path):
            continue
        yield path
