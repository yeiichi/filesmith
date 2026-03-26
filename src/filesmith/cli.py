from __future__ import annotations

import argparse
from typing import Sequence

from .cli_findmove import add_find_move_subparser
from .cli_knapsack import add_knapsack_subparser


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="filesmith")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_find_move_subparser(subparsers)
    add_knapsack_subparser(subparsers)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if hasattr(args, "func"):
        return args.func(args)

    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())