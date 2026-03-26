from pathlib import Path
import shutil
from filesmith.knapsack import run_knapsack, select_files_by_capacity, copy_files_by_capacity


def test_run_knapsack_exact_match():
    items = [4, 7, 2, 9, 5]
    best_sum, subset_indices = run_knapsack(items, 11)

    assert best_sum == 11
    assert sum(items[i] for i in subset_indices) == 11
    assert all(items[i] in [4, 7, 2, 9, 5] for i in subset_indices)


def test_run_knapsack_ignores_invalid_items():
    items = [-3, 0, 2, 6, 20]
    best_sum, subset_indices = run_knapsack(items, 7)

    assert best_sum == 6
    assert sum(items[i] for i in subset_indices) == 6
    # items[i] should be 6, or three 2s if we had more 2s.
    # In this case we have one 2 and one 6.
    assert [items[i] for i in subset_indices] == [6]


def test_run_knapsack_empty_result():
    best_sum, subset = run_knapsack([10, 20, 30], 5)

    assert best_sum == 0
    assert subset == []


def test_run_knapsack_zero_capacity():
    best_sum, subset = run_knapsack([1, 2, 3], 0)

    assert best_sum == 0
    assert subset == []


def test_run_knapsack_negative_capacity():
    try:
        run_knapsack([1, 2, 3], -1)
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_select_files_by_capacity(tmp_path):
    # Setup some files with specific sizes
    f1 = tmp_path / "f1.bin"
    f2 = tmp_path / "f2.bin"
    f3 = tmp_path / "f3.bin"

    f1.write_bytes(b"A" * 10)
    f2.write_bytes(b"B" * 20)
    f3.write_bytes(b"C" * 30)

    files = [f1, f2, f3]
    # Capacity 35 should select f1 (10) and f2 (20) = 30
    best_sum, selected = select_files_by_capacity(files, 35)

    assert best_sum == 30
    assert len(selected) == 2
    assert set(selected) == {f1, f2}


def test_copy_files_by_capacity(tmp_path):
    src_dir = tmp_path / "src"
    dest_dir = tmp_path / "dest"
    src_dir.mkdir()
    dest_dir.mkdir()

    f1 = src_dir / "foo.txt"
    f2 = src_dir / "bar.txt"
    f3 = src_dir / "baz.txt"

    f1.write_bytes(b"1" * 5)
    f2.write_bytes(b"2" * 3)
    f3.write_bytes(b"3" * 10)

    # Capacity 9 should select f1 (5) and f2 (3) = 8
    total_size, ops = copy_files_by_capacity(src_dir, dest_dir, 9)

    assert total_size == 8
    assert len(ops) == 2
    copied_names = {src.name for src, dest in ops}
    assert copied_names == {"foo.txt", "bar.txt"}

    # Verify files exist in destination
    assert (dest_dir / "foo.txt").exists()
    assert (dest_dir / "bar.txt").exists()
    assert not (dest_dir / "baz.txt").exists()