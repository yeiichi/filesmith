#!/usr/bin/env python3
"""
cli_findmove.py — small CLI wrapper around FindMoveJob.

Console script name (suggested):
    filesmith-find-move
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .engine import FindMoveJob


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="filesmith-find-move",
        description="Find files and copy/move them using filesmith.",
    )

    parser.add_argument(
        "src",
        help="Source directory to search.",
    )
    parser.add_argument(
        "dst",
        help="Destination directory to copy/move files into.",
    )
    parser.add_argument(
        "-p",
        "--pattern",
        default="*",
        help="Glob pattern for matching files (default: '*'). Example: '*.txt'",
    )
    parser.add_argument(
        "-m",
        "--mode",
        choices=["copy", "move"],
        default="copy",
        help="Operation mode: copy or move (default: copy).",
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Show what would be done, without touching the filesystem.",
    )
    parser.add_argument(
        "-R",
        "--no-recursive",
        dest="recursive",
        action="store_false",
        help="Do NOT search directories recursively (default is recursive).",
    )

    parser.set_defaults(recursive=True)

    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)

    job = FindMoveJob(
        src_root=Path(args.src),
        dest_root=Path(args.dst),
        pattern=args.pattern,
        recursive=args.recursive,
        mode=args.mode,
        dry_run=args.dry_run,
    )

    ops = job.run()

    # Simple, user-friendly output
    if args.dry_run:
        for src, dst in ops:
            print(f"[DRY-RUN] {src} -> {dst}")
    else:
        for src, dst in ops:
            print(f"{src} -> {dst}")

    print(f"{len(ops)} file(s) processed.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
