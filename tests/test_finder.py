from collections.abc import Iterator
from pathlib import Path

from filesmith.finder import find_files


def test_find_files_non_recursive(tmp_path: Path):
    (tmp_path / "a.txt").write_text("hello")
    (tmp_path / "b.txt").write_text("world")
    (tmp_path / "c.md").write_text("markdown")
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "inner.txt").write_text("inside")

    results = list(find_files(tmp_path, glob_pattern="*.txt", recursive=False))

    names = sorted([p.name for p in results])
    assert names == ["a.txt", "b.txt"]


def test_find_files_recursive(tmp_path: Path):
    sub = tmp_path / "sub"
    sub.mkdir()
    (tmp_path / "outer.txt").write_text("outside")
    (sub / "inner.txt").write_text("inside")

    results = list(find_files(tmp_path, glob_pattern="*.txt", recursive=True))

    names = sorted([p.name for p in results])
    assert names == ["inner.txt", "outer.txt"]


def test_find_files_glob_pattern_matching(tmp_path: Path):
    (tmp_path / "alpha.py").write_text("print('alpha')")
    (tmp_path / "beta.py").write_text("print('beta')")
    (tmp_path / "alpha.txt").write_text("alpha")

    results = list(find_files(tmp_path, glob_pattern="alpha.*", recursive=False))

    names = sorted([p.name for p in results])
    assert names == ["alpha.py", "alpha.txt"]


def test_find_files_predicate(tmp_path: Path):
    (tmp_path / "x.txt").write_text("hello")
    (tmp_path / "y.txt").write_text("world")

    def pred(path: Path) -> bool:
        return path.read_text().startswith("h")

    results = list(find_files(tmp_path, glob_pattern="*.txt", predicate=pred))

    assert len(results) == 1
    assert results[0].name == "x.txt"


def test_find_files_accepts_string_root(tmp_path: Path):
    (tmp_path / "a.txt").write_text("hello")

    results = list(find_files(str(tmp_path), glob_pattern="*.txt", recursive=False))

    assert [p.name for p in results] == ["a.txt"]


def test_find_files_returns_lazy_iterator(tmp_path: Path):
    (tmp_path / "a.txt").write_text("hello")
    seen: list[str] = []

    def pred(path: Path) -> bool:
        seen.append(path.name)
        return True

    results = find_files(tmp_path, glob_pattern="*.txt", predicate=pred)

    assert isinstance(results, Iterator)
    assert seen == []
    assert [p.name for p in results] == ["a.txt"]
    assert seen == ["a.txt"]


def test_find_files_keeps_pattern_keyword_for_compatibility(tmp_path: Path):
    (tmp_path / "a.txt").write_text("hello")

    results = list(find_files(tmp_path, pattern="*.txt", recursive=False))

    assert [p.name for p in results] == ["a.txt"]
