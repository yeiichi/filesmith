"""
engine.py — orchestration layer (thin wrapper).

This module connects:
- finder.find_files()
- transfer.transfer_files()

into a structured "job" class.  `core.py` can delegate to this
gradually without breaking backward compatibility.
"""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional

from .finder import find_files
from .transfer import transfer_files


@dataclass
class FindMoveJob:
    src_root: Path
    dest_root: Path
    pattern: str = "*"
    recursive: bool = True
    mode: Literal["copy", "move"] = "copy"
    dry_run: bool = False

    # Future extensions: predicate, conflict policy, logging, etc.

    def run(self):
        files = find_files(
            self.src_root,
            pattern=self.pattern,
            recursive=self.recursive,
        )

        return transfer_files(
            files,
            self.dest_root,
            mode=self.mode,
            dry_run=self.dry_run,
        )
