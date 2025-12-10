import argparse
import datetime
import logging
import os
import re
import shutil
from pathlib import Path

from .transfer import transfer_files


def _get_mtime_threshold(newermt_value):
    """
    Retrieves a modification time (mtime) threshold based on the provided input.

    The function attempts to derive an mtime threshold based on a given value.
    It first checks if the input is empty and returns 0. If a value is provided,
    it tries to interpret the value as a file path to retrieve its last modification
    time using os.path.getmtime(). If the file does not exist, it then attempts to
    parse the value as an ISO 8601 date/datetime string and converts it to a
    Unix timestamp. If both interpretations fail, it raises a ValueError.

    Parameters:
        newermt_value (str): The input value to derive the mtime threshold. This may
        represent either a file path or an ISO 8601 date/datetime string.

    Returns:
        float: The derived modification time as a Unix timestamp. Returns 0 if
        no value is provided.

    Raises:
        ValueError: If the input is neither a valid file path with a retrievable mtime
        nor a valid ISO 8601 date/datetime string.
    """
    if not newermt_value:
        return 0
    try:
        return os.path.getmtime(newermt_value)
    except FileNotFoundError:
        try:
            return datetime.datetime.fromisoformat(newermt_value).timestamp()
        except ValueError:
            raise ValueError(
                f"Error: --newermt value is not a valid file or ISO date/datetime: {newermt_value}"
            )


def _ensure_destination_exists(destination, dry_run):
    if os.path.isdir(destination):
        return
    if dry_run:
        logging.info("(Dry Run) Would create destination directory: %s", destination)
    else:
        os.makedirs(destination)


def _copy_file_action(source_path, destination_path, dry_run, quiet):
    if dry_run:
        logging.info("(Dry Run) Would copy: %s to %s", source_path, destination_path)
        return
    try:
        shutil.copy2(source_path, destination_path)
        if not quiet:
            logging.info("Copied: %s", source_path)
    except FileNotFoundError:
        pass


def copy_files(origin, destination, pattern, newermt=None, dry_run=False, quiet=False):
    """
    Copies files from origin to destination based on a regex pattern.
    """
    # Normalize paths (accept both str and Path)
    origin_path = Path(origin).expanduser()
    destination_path = Path(destination).expanduser()

    _ensure_destination_exists(destination_path, dry_run)
    try:
        mtime_threshold = _get_mtime_threshold(newermt)
    except ValueError as e:
        logging.error(str(e))
        return

    selected_files: list[Path] = []

    # Keep existing behavior:
    # - Walk the directory tree with os.walk
    # - Filter filenames by regex (`pattern`)
    # - Apply mtime threshold if provided
    for dirpath, _, filenames in os.walk(origin_path):
        for filename in filenames:
            if not re.search(pattern, filename):
                continue

            source_path = Path(dirpath) / filename
            if mtime_threshold and source_path.stat().st_mtime <= mtime_threshold:
                continue

            selected_files.append(source_path)

    if not selected_files:
        return

    # Delegate the actual copying to the new transfer layer.
    # Previous behavior: last writer wins if filenames collide -> use overwrite.
    ops = transfer_files(
        selected_files,
        destination_path,
        mode="copy",
        on_conflict="overwrite",
        dry_run=dry_run,
    )

    # Preserve logging semantics:
    # - Previously, dry-run always logged (ignoring quiet)
    # - For real copies, quiet suppressed per-file "Copied: ..." logs

    if dry_run:
        # Always log in dry-run mode (even if quiet=True), as before
        for src, dst in ops:
            logging.info("(Dry Run) Would copy: %s to %s", src, dst)
    else:
        if quiet:
            return
        for src, _dst in ops:
            logging.info("Copied: %s", src)


def get_target_file(src_dir: str | Path, target_key: str, ext: str | None = None) -> Path:
    """Return exactly one file in `src_dir` that contains `target_key` in the filename."""
    src = Path(src_dir).expanduser().resolve()

    if not src.exists() or not src.is_dir():
        raise ValueError(f"Directory not found: {src}")

    pattern = f"*{ext}" if ext else "*"
    files = [p for p in sorted(src.glob(pattern)) if target_key in p.name]

    if len(files) == 0:
        raise ValueError(f"No file found with key={target_key!r} in {src}")
    if len(files) > 1:
        raise ValueError(
            f"Multiple files found with key={target_key!r} in {src}:\n" +
            "\n".join(str(f) for f in files)
        )

    return files[0]


def main():
    """
    Main function to parse arguments and call the copy_files function.
    """
    parser = argparse.ArgumentParser(
        description="Copies files based on filename pattern."
    )
    parser.add_argument("origin", help="Origin directory")
    parser.add_argument("destination", help="Destination directory")
    parser.add_argument("pattern", help="Regex pattern for filenames")
    parser.add_argument(
        "--newermt",
        help="Copy only files newer than the specified file's modification time or a given ISO date/datetime.",
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Show what files would be copied without actually copying them.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress output of successfully copied files. Useful for cron jobs.",
    )
    args = parser.parse_args()
    copy_files(
        args.origin,
        args.destination,
        args.pattern,
        args.newermt,
        args.dry_run,
        args.quiet,
    )


if __name__ == "__main__":
    main()
