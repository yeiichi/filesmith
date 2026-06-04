from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .duplicates import (
    find_duplicate_files,
    format_duplicate_report,
    summarize_duplicate_groups,
    write_duplicate_report,
)


def add_duplicates_subparser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser(
        "duplicates",
        help="Find duplicate files by SHA-256 digest.",
    )
    _add_arguments(parser)
    parser.set_defaults(func=_run_duplicates)


def _add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("root", help="Root directory to walk.")
    parser.add_argument(
        "--maxdepth",
        type=int,
        required=True,
        help="Maximum directory depth to scan. Use 0 for files directly in root.",
    )
    parser.add_argument(
        "-p",
        "--pattern",
        default="*",
        help="Glob pattern for matching files (default: '*').",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="filesmith-duplicates.txt",
        help="Path for the machine-friendly text report.",
    )


def _run_duplicates(args: argparse.Namespace) -> int:
    root = Path(args.root)
    groups = find_duplicate_files(root, maxdepth=args.maxdepth, pattern=args.pattern)
    write_duplicate_report(
        groups,
        root=root,
        maxdepth=args.maxdepth,
        output_path=Path(args.output),
    )

    print(summarize_duplicate_groups(groups))
    print(f"report: {Path(args.output).expanduser()}")
    if groups:
        print()
        print(format_duplicate_report(groups, root=root, maxdepth=args.maxdepth), end="")

    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="filesmith-duplicates",
        description="Find duplicate files by SHA-256 digest.",
    )
    _add_arguments(parser)
    args = parser.parse_args(argv)
    return _run_duplicates(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
