from pathlib import Path

from filesmith.duplicates import (
    find_duplicate_files,
    format_duplicate_report,
    walk_files,
    write_duplicate_report,
)


def test_walk_files_respects_maxdepth(tmp_path: Path):
    (tmp_path / "root.txt").write_text("root")
    level_1 = tmp_path / "level-1"
    level_1.mkdir()
    (level_1 / "child.txt").write_text("child")
    level_2 = level_1 / "level-2"
    level_2.mkdir()
    (level_2 / "grandchild.txt").write_text("grandchild")

    assert [path.name for path in walk_files(tmp_path, maxdepth=0)] == ["root.txt"]
    assert [path.name for path in walk_files(tmp_path, maxdepth=1)] == [
        "child.txt",
        "root.txt",
    ]


def test_find_duplicate_files_groups_matching_digests(tmp_path: Path):
    (tmp_path / "a.txt").write_text("same")
    (tmp_path / "b.txt").write_text("same")
    (tmp_path / "unique.txt").write_text("different")

    groups = find_duplicate_files(tmp_path, maxdepth=0)

    assert len(groups) == 1
    assert groups[0].size == 4
    assert [duplicate_file.path.name for duplicate_file in groups[0].files] == [
        "a.txt",
        "b.txt",
    ]


def test_duplicate_report_format_is_machine_friendly(tmp_path: Path):
    (tmp_path / "a.txt").write_text("same")
    (tmp_path / "b.txt").write_text("same")
    groups = find_duplicate_files(tmp_path, maxdepth=0)

    report = format_duplicate_report(groups, root=tmp_path, maxdepth=0)

    assert report.startswith("# filesmith duplicate report v1\n")
    assert "duplicate_groups\t1\n" in report
    assert "duplicate_files\t2\n" in report
    assert "\ngroup\t1\tsha256\t" in report
    assert f"\nfile\t1\t4\t{tmp_path / 'a.txt'}\n" in report


def test_write_duplicate_report_creates_parent_directories(tmp_path: Path):
    (tmp_path / "a.txt").write_text("same")
    (tmp_path / "b.txt").write_text("same")
    groups = find_duplicate_files(tmp_path, maxdepth=0)
    output_path = tmp_path / "reports" / "duplicates.txt"

    written_path = write_duplicate_report(
        groups,
        root=tmp_path,
        maxdepth=0,
        output_path=output_path,
    )

    assert written_path == output_path
    assert output_path.exists()
    assert "duplicate_groups\t1\n" in output_path.read_text()
