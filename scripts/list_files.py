#!/usr/bin/env python3
import argparse
import csv
import hashlib
import time
from datetime import datetime
from pathlib import Path


def human_size(num_bytes: int) -> str:
    for unit in ["B", "K", "M", "G", "T", "P"]:
        if num_bytes < 1024:
            return f"{num_bytes:.1f}{unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f}E"


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def scan_dir(target: Path):
    for p in sorted(target.iterdir()):
        if p.is_file():
            stat = p.stat()
            yield {
                "filename": p.name,
                "suffix": p.suffix,
                "size_bytes": stat.st_size,
                "size_human": human_size(stat.st_size),
                "modified": datetime.fromtimestamp(stat.st_mtime)
                .isoformat(sep=" ", timespec="seconds"),
                "sha256": sha256_of(p),
            }


def write_csv(rows, output_csv: Path):
    with output_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def print_table(rows):
    # Compute column widths
    col_widths = {
        k: max(len(k), *(len(str(r[k])) for r in rows))
        for k in rows[0].keys()
    }

    # Header
    header = "  ".join(k.ljust(col_widths[k]) for k in col_widths)
    print(header)
    print("-" * len(header))

    # Rows
    for r in rows:
        print("  ".join(str(r[k]).ljust(col_widths[k]) for k in col_widths))


def timestamp_filename(base: str = "file_list", ext: str = ".csv") -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base}_{ts}{ext}"


def epoch_filename(base: str = "file_list", ext: str = ".csv") -> str:
    ep = int(time.time())  # Unix epoch seconds
    return f"{base}_{ep}{ext}"


def main():
    parser = argparse.ArgumentParser(description="List files and export info as CSV.")
    parser.add_argument("target", help="Directory to scan")
    parser.add_argument("-o", "--output", help="Output CSV filename")
    parser.add_argument("--epoch", action="store_true",
                        help="Use epoch time in output filename")
    args = parser.parse_args()

    target = Path(args.target).expanduser()
    if not target.is_dir():
        raise ValueError(f"Not a directory: {target}")

    rows = list(scan_dir(target))

    if not rows:
        print("No files found.")
        return

    print_table(rows)

    # Decide output filename
    if args.output:
        output_csv = Path(args.output)
    else:
        output_csv = Path(epoch_filename() if args.epoch else timestamp_filename())

    write_csv(rows, output_csv)
    print(f"\nCSV saved to: {output_csv}")


if __name__ == "__main__":
    main()
