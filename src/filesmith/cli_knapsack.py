from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .knapsack import copy_files_by_capacity, run_knapsack


def add_knapsack_subparser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    knapsack_parser = subparsers.add_parser(
        "knapsack",
        help="Knapsack-related operations.",
    )
    knapsack_subparsers = knapsack_parser.add_subparsers(
        dest="knapsack_command",
        required=True,
    )

    copy_parser = knapsack_subparsers.add_parser(
        "copy",
        help="Copy a subset of files from a source directory into a destination directory.",
    )
    copy_parser.add_argument("src_dir", help="Source directory")
    copy_parser.add_argument("dest_dir", help="Destination directory")
    copy_parser.add_argument("capacity", type=int, help="Maximum total size in bytes")
    copy_parser.add_argument(
        "-p",
        "--pattern",
        default="*",
        help="Glob pattern for matching files (default: '*')",
    )
    copy_parser.add_argument(
        "-R",
        "--no-recursive",
        dest="recursive",
        action="store_false",
        help="Do NOT search recursively (default is recursive).",
    )
    copy_parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Show what would be copied without copying anything.",
    )
    copy_parser.set_defaults(recursive=True)
    copy_parser.set_defaults(func=_run_copy)

    solve_parser = knapsack_subparsers.add_parser(
        "solve",
        help="Solve a knapsack/subset-sum problem for integer items.",
    )
    solve_parser.add_argument("capacity", type=int, help="Maximum capacity / target sum")
    solve_parser.add_argument("items", nargs="+", type=int, help="Item values")
    solve_parser.set_defaults(func=_run_solve)


def _run_copy(args: argparse.Namespace) -> int:
    total_size, ops = copy_files_by_capacity(
        Path(args.src_dir),
        Path(args.dest_dir),
        args.capacity,
        pattern=args.pattern,
        recursive=args.recursive,
        dry_run=args.dry_run,
    )

    for src, dst in ops:
        prefix = "[DRY-RUN] " if args.dry_run else ""
        print(f"{prefix}{src} -> {dst}")

    print(f"selected_total_size: {total_size}")
    print(f"{len(ops)} file(s) processed.")
    return 0


def _run_solve(args: argparse.Namespace) -> int:
    best_sum, subset = run_knapsack(args.items, args.capacity)
    print(f"best_sum: {best_sum}")
    print(f"subset: {subset}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="filesmith-knapsack",
        description="Knapsack-related operations.",
    )
    subparsers = parser.add_subparsers(
        dest="knapsack_command",
        required=True,
    )

    copy_parser = subparsers.add_parser(
        "copy",
        help="Copy a subset of files from a source directory into a destination directory.",
    )
    copy_parser.add_argument("src_dir", help="Source directory")
    copy_parser.add_argument("dest_dir", help="Destination directory")
    copy_parser.add_argument("capacity", type=int, help="Maximum total size in bytes")
    copy_parser.add_argument(
        "-p",
        "--pattern",
        default="*",
        help="Glob pattern for matching files (default: '*')",
    )
    copy_parser.add_argument(
        "-R",
        "--no-recursive",
        dest="recursive",
        action="store_false",
        help="Do NOT search recursively (default is recursive).",
    )
    copy_parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Show what would be copied without copying anything.",
    )
    copy_parser.set_defaults(recursive=True)
    copy_parser.set_defaults(func=_run_copy)

    solve_parser = subparsers.add_parser(
        "solve",
        help="Solve a knapsack/subset-sum problem for integer items.",
    )
    solve_parser.add_argument("capacity", type=int, help="Maximum capacity / target sum")
    solve_parser.add_argument("items", nargs="+", type=int, help="Item values")
    solve_parser.set_defaults(func=_run_solve)

    args = parser.parse_args(argv)

    if hasattr(args, "func"):
        return args.func(args)

    return 1