import shutil
from pathlib import Path
from filesmith.finder import find_files


def test_find_files_basic(tmp_path: Path):
    # Setup
    (tmp_path / "a.txt").write_text("hello")
    (tmp_path / "b.txt").write_text("world")
    (tmp_path / "c.md").write_text("markdown")

    # Exercise
    results = find_files(tmp_path, pattern="*.txt", recursive=False)

    # Verify
    names = sorted([p.name for p in results])
    assert names == ["a.txt", "b.txt"]


def test_find_files_recursive(tmp_path: Path):
    # Setup
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "inner.txt").write_text("inside")

    # Exercise
    results = find_files(tmp_path, pattern="*.txt", recursive=True)

    # Verify
    assert any(p.name == "inner.txt" for p in results)


def test_find_files_predicate(tmp_path: Path):
    (tmp_path / "x.txt").write_text("hello")
    (tmp_path / "y.txt").write_text("world")

    # Predicate: keep only files whose content starts with 'h'
    def pred(path: Path):
        return path.read_text().startswith("h")

    results = find_files(tmp_path, pattern="*.txt", predicate=pred)

    assert len(results) == 1
    assert results[0].name == "x.txt"
