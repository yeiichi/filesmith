# Filesmith

[![PyPI version](https://img.shields.io/pypi/v/filesmith.svg)](https://pypi.org/project/filesmith/)
![Python versions](https://img.shields.io/pypi/pyversions/filesmith.svg)
[![License](https://img.shields.io/pypi/l/filesmith.svg)](https://pypi.org/project/filesmith/)

A collection of file manipulation and inspection utilities, including pattern-based file operations and knapsack-based file selection.

## Installation

You can install filesmith using pip:

```bash
pip install filesmith
```

## Usage (CLI)

Filesmith provides a unified CLI with subcommands.

```bash
filesmith <command> [arguments] [options]
```

### 1. `find-move`

Find files and copy/move them.

```bash
filesmith find-move <src> <dst> [-p PATTERN] [-m {copy,move}] [-n] [-R]
```

- `src`: Source directory.
- `dst`: Destination directory.
- `-p`, `--pattern`: Glob pattern (default: `*`).
- `-m`, `--mode`: `copy` or `move` (default: `copy`).
- `-n`, `--dry-run`: Show what would be done.
- `-R`, `--no-recursive`: Do NOT search recursively.

**Example:**
```bash
filesmith find-move ./src ./backup -p "*.py"
```

### 2. `knapsack`

Knapsack-related operations.

#### `copy`
Copy a subset of files to a destination without exceeding a total size capacity.

```bash
filesmith knapsack copy <src_dir> <dest_dir> <capacity> [-p PATTERN] [-n] [-R]
```

**Example:**
```bash
# Copy up to 100MB of images
filesmith knapsack copy ./photos ./usb-drive 104857600 -p "*.jpg"
```

#### `solve`
Solve a general knapsack/subset-sum problem for integer items.

```bash
filesmith knapsack solve <capacity> <items...>
```

### 3. Legacy CLI

The original regex-based copy tool is available via:

```bash
filesmith-legacy copy <origin> <destination> <pattern> [--newermt REF] [-n] [-q]
```

## Python API

Filesmith can also be used as a Python library.

### File Operations

#### `find_files` & `transfer_files`
Modern, structured way to find and move/copy files.

```python
from pathlib import Path
from filesmith import find_files, transfer_files

# Find all Python files recursively
files = find_files(Path("./src"), pattern="*.py", recursive=True)

# Transfer them to a backup folder (copy or move)
transfer_files(files, Path("./backup"), mode="copy", on_conflict="skip")
```

#### `FindMoveJob`
An orchestration class for "find and transfer" operations.

```python
from pathlib import Path
from filesmith import FindMoveJob

job = FindMoveJob(
    src_root=Path("./src"),
    dest_root=Path("./dst"),
    pattern="*.txt",
    mode="move"
)
job.run()
```

#### `get_target_file`
Finds exactly one file in a directory that matches a key and optional extension. Throws `ValueError` if zero or multiple files are found.

```python
from filesmith import get_target_file

# Returns a Path object if unique match found
path = get_target_file("./data", "report_2023", ext=".csv")
print(f"Found unique report: {path.name}")
```

#### `copy_files` (Legacy)
Regex-based copy tool with optional modification time filtering.

```python
from filesmith import copy_files

# Copy files matching a regex, newer than a specific date
copy_files(
    origin="./logs",
    destination="./archive",
    pattern=r"error_.*\.log",
    newermt="2023-01-01"
)
```

### Optimization & Knapsack

#### `copy_files_by_capacity`
Copies a subset of files that fit within a specified byte capacity. Useful for filling external drives.

```python
from filesmith import copy_files_by_capacity

total_size, ops = copy_files_by_capacity(
    src_dir="./photos",
    dest_dir="/mnt/usb",
    capacity=1024 * 1024 * 700  # 700 MB
)
print(f"Filled {total_size} bytes across {len(ops)} files.")
```

#### `run_knapsack`
General-purpose subset-sum solver for integer items.

```python
from filesmith import run_knapsack

items = [10, 20, 30, 40, 50]
capacity = 65
best_sum, indices = run_knapsack(items, capacity)

# best_sum: 60, indices: [4, 0] (50 + 10) or similar
```

---

## Changelog

### 0.4.1
- Enriched Python API documentation with practical usage examples.

### 0.4.0
- Added unified `filesmith` command with subcommands: `find-move`, `knapsack`.
- Added `filesmith-legacy` for the previous regex-based CLI.
- Expanded Python API in `filesmith` package.
- Improved internal structure (finder, transfer, engine).

### 0.2.0
- Added `get_target_file` utility.
- Improved `copy_files` with structured logging and `--newermt` filtering.
