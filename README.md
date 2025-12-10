# Filesmith

[![PyPI version](https://img.shields.io/pypi/v/filesmith.svg)](https://pypi.org/project/filesmith/)
![Python versions](https://img.shields.io/pypi/pyversions/filesmith.svg)
[![License](https://img.shields.io/pypi/l/filesmith.svg)](https://pypi.org/project/filesmith/)

A command-line utility for copying files based on pattern matching, with support for filtering by modification time, plus a helper function for selecting uniquely matched files.

## Overview

Filesmith is a Python utility that helps you copy files from one directory to another based on regular expression
patterns. It's particularly useful for selective file copying, backup operations, and automated file management tasks.

It also includes `get_target_file`, a reliable helper for retrieving a single uniquely identified file by substring and optional extension filter.

## Installation

You can install filesmith using pip:

```bash
pip install filesmith
```

## Usage (CLI)

```bash
filesmith <origin> <destination> <pattern> [options]
```

### Arguments
- `origin`: The source directory.
- `destination`: The destination directory.
- `pattern`: The regex pattern to match filenames against.

### Options
- `--newermt <file_or_isodate>`: Only copy files newer than a reference file's modification time or a given ISO date/datetime.
- `-n`, `--dry-run`: Show which files would be copied without actually copying them.
- `-q`, `--quiet`: Suppress output for successfully copied files.

### Examples

1.  **Copy all .txt files from `source` to `dest`:**
    ```bash
    filesmith /path/to/source /path/to/dest ".*\.txt$"
    ```

2.  **Perform a dry run to see which .jpg files would be copied:**
    ```bash
    filesmith /path/to/source /path/to/dest ".*\.jpg$" --dry-run
    ```

3.  **Copy .log files newer than a specific date:**
    ```bash
    filesmith /path/to/logs /path/to/backup ".*\.log$" --newermt 2023-10-27T10:00:00
    ```

4.  **Copy .py files that are newer than `main.py`:**
    ```bash
    filesmith /path/to/src /path/to/old_src ".*\.py$" --newermt /path/to/src/main.py
    ```

---

## Python Utility: `get_target_file`

Filesmith includes a small but powerful helper function to locate **exactly one** matching file in a directory.

### Usage

```python
from filesmith import get_target_file

file_path = get_target_file("/path/to/dir", "report", ".xlsx")
print(file_path)
```

### Features

- Ensures **exactly one** match.
- Raises `ValueError` if:
  - No files match.
  - More than one file matches.
- Optional extension filtering:
  ```python
  get_target_file("data", "2024", ".csv")
  ```

This is ideal when processing pipelines rely on single expected inputs, such as weekly exports or naming‑convention‑based file detection.

---

## Changelog

### 0.2.0
- Added `get_target_file` utility.
- Improved `copy_files`:
  - Switched from `print` to structured `logging`.
  - More robust handling of ISO datetime / file-based `--newermt` filtering.
- Extended full test coverage (`pytest`).

### 0.3.0
- Added new CLI: `filesmith-find-move`
- Integrated core.copy_files with the new engine (finder / transfer / FindMoveJob)
