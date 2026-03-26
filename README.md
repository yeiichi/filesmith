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

```python
from pathlib import Path
from filesmith import get_target_file, copy_files, find_files, FindMoveJob

# Locate a unique file
path = get_target_file("./data", "report", ".xlsx")

# Use the new job engine
job = FindMoveJob(src_root=Path("./src"), dest_root=Path("./dst"), pattern="*.txt")
job.run()
```

### Key Functions

- `get_target_file(dir, key, ext)`: Finds exactly one matching file.
- `find_files(root, pattern, recursive, predicate)`: Advanced file finding.
- `copy_files(origin, destination, pattern, ...)`: Regex-based copy (legacy).
- `run_knapsack(items, capacity)`: Solves the subset-sum problem.
- `copy_files_by_capacity(src, dest, capacity, ...)`: Size-constrained copying.

---

## Changelog

### 0.4.0
- Refactored CLI into a unified `filesmith` command with subcommands: `find-move`, `knapsack`.
- Added `filesmith-legacy` for the previous regex-based CLI.
- Expanded Python API in `filesmith` package.
- Improved internal structure (finder, transfer, engine).

### 0.3.0
- Added new CLI: `filesmith-find-move`.
- Integrated `core.copy_files` with the new engine.

### 0.2.0
- Added `get_target_file` utility.
- Improved `copy_files` with structured logging and `--newermt` filtering.
