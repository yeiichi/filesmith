from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatch
import os
from pathlib import Path
from typing import Iterable, Sequence

from smith_utils.crypto import get_file_digest


@dataclass(frozen=True)
class DuplicateFile:
    path: Path
    size: int


@dataclass(frozen=True)
class DuplicateGroup:
    digest: str
    size: int
    files: tuple[DuplicateFile, ...]


def walk_files(root: Path, maxdepth: int, pattern: str = "*") -> list[Path]:
    if maxdepth < 0:
        raise ValueError("maxdepth must be greater than or equal to 0")

    root = Path(root).expanduser()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Directory not found: {root}")

    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        current_dir = Path(dirpath)
        depth = len(current_dir.relative_to(root).parts)
        if depth >= maxdepth:
            dirnames.clear()
        if depth > maxdepth:
            continue
        for filename in filenames:
            if fnmatch(filename, pattern):
                files.append(current_dir / filename)

    return sorted(files)


def find_duplicate_files(
    root: Path,
    maxdepth: int,
    pattern: str = "*",
) -> list[DuplicateGroup]:
    files = walk_files(root, maxdepth=maxdepth, pattern=pattern)
    by_digest: dict[str, list[DuplicateFile]] = {}

    for path in files:
        digest = get_file_digest(path)
        duplicate_file = DuplicateFile(path=path, size=path.stat().st_size)
        by_digest.setdefault(digest, []).append(duplicate_file)

    groups: list[DuplicateGroup] = []
    for digest, digest_files in by_digest.items():
        if len(digest_files) < 2:
            continue
        ordered_files = tuple(sorted(digest_files, key=lambda item: str(item.path)))
        groups.append(
            DuplicateGroup(
                digest=digest,
                size=ordered_files[0].size,
                files=ordered_files,
            )
        )

    return sorted(groups, key=lambda group: (group.size, group.digest), reverse=True)


def format_duplicate_report(
    groups: Sequence[DuplicateGroup],
    root: Path,
    maxdepth: int,
) -> str:
    duplicate_file_count = sum(len(group.files) for group in groups)
    wasted_bytes = sum((len(group.files) - 1) * group.size for group in groups)
    lines = [
        "# filesmith duplicate report v1",
        f"root\t{Path(root).expanduser()}",
        f"maxdepth\t{maxdepth}",
        f"duplicate_groups\t{len(groups)}",
        f"duplicate_files\t{duplicate_file_count}",
        f"wasted_bytes\t{wasted_bytes}",
    ]

    for index, group in enumerate(groups, start=1):
        lines.append(
            f"group\t{index}\tsha256\t{group.digest}\tsize\t{group.size}\tcount\t{len(group.files)}"
        )
        for duplicate_file in group.files:
            lines.append(f"file\t{index}\t{duplicate_file.size}\t{duplicate_file.path}")

    return "\n".join(lines) + "\n"


def write_duplicate_report(
    groups: Sequence[DuplicateGroup],
    root: Path,
    maxdepth: int,
    output_path: Path,
) -> Path:
    output_path = Path(output_path).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        format_duplicate_report(groups, root=root, maxdepth=maxdepth),
        encoding="utf-8",
    )
    return output_path


def summarize_duplicate_groups(groups: Iterable[DuplicateGroup]) -> str:
    group_list = list(groups)
    duplicate_file_count = sum(len(group.files) for group in group_list)
    wasted_bytes = sum((len(group.files) - 1) * group.size for group in group_list)
    return (
        f"duplicate_groups: {len(group_list)}\n"
        f"duplicate_files: {duplicate_file_count}\n"
        f"wasted_bytes: {wasted_bytes}"
    )
