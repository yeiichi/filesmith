from __future__ import annotations
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Sequence


def run_knapsack(items: list[int], capacity: int) -> tuple[int, list[int]]:
    """
    Pure Python implementation of the subset sum problem.
    Returns (best_sum, list_of_indices).
    """
    if capacity < 0:
        raise ValueError("capacity must be non-negative")

    # Filter items to optimize (keep original indices)
    # filtered: list of (original_index, size)
    filtered = [(i, item) for i, item in enumerate(items) if 0 < item <= capacity]
    filtered.sort(key=lambda x: x[1])

    # reachable[s] is True if sum 's' is reachable
    reachable = [False] * (capacity + 1)
    reachable[0] = True

    # To reconstruct the subset, we store which item was used to reach each sum
    # parent[s] = index in 'filtered' of the item used to reach sum 's', or -1
    parent = [-1] * (capacity + 1)

    for i, (_, item_size) in enumerate(filtered):
        for s in range(capacity, item_size - 1, -1):
            if not reachable[s] and reachable[s - item_size]:
                reachable[s] = True
                parent[s] = i

    # Find the largest reachable sum
    best_sum = 0
    for s in range(capacity, -1, -1):
        if reachable[s]:
            best_sum = s
            break

    # Reconstruct the subset (list of original indices)
    subset_indices = []
    curr = best_sum
    while curr > 0:
        f_idx = parent[curr]
        if f_idx == -1:
            break
        orig_idx, item_size = filtered[f_idx]
        subset_indices.append(orig_idx)
        curr -= item_size

    return best_sum, subset_indices


def select_files_by_capacity(files: list[Path], capacity: int) -> tuple[int, list[Path]]:
    """
    Select a subset of files whose total size is closest to (but not exceeding) capacity.
    """
    sizes = [f.stat().st_size for f in files]
    best_sum, indices = run_knapsack(sizes, capacity)
    selected_files = [files[i] for i in indices]
    return best_sum, selected_files


def copy_files_by_capacity(
    src_dir: str | Path,
    dest_dir: str | Path,
    capacity: int,
    pattern: str = "*",
    recursive: bool = True,
    dry_run: bool = False,
) -> tuple[int, list[tuple[Path, Path]]]:
    """
    Find files in src_dir, select a subset whose total size is <= capacity,
    and copy them to dest_dir.
    """
    from filesmith.finder import find_files
    from filesmith.transfer import transfer_files

    src_dir = Path(src_dir).expanduser()
    dest_dir = Path(dest_dir).expanduser()

    # 1. Find all files
    all_files = find_files(src_dir, pattern=pattern, recursive=recursive)

    # 2. Select files by capacity
    total_size, selected_files = select_files_by_capacity(all_files, capacity)

    # 3. Copy selected files
    ops = transfer_files(
        selected_files,
        dest_dir,
        mode="copy",
        on_conflict="skip",
        dry_run=dry_run,
    )

    return total_size, ops