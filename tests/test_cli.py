import pytest
from filesmith.cli import main

def test_cli_help(capfd):
    with pytest.raises(SystemExit) as excinfo:
        main(["--help"])
    assert excinfo.value.code == 0
    out, err = capfd.readouterr()
    assert "usage: filesmith" in out
    assert "find-move" in out
    assert "knapsack" in out
    assert "duplicates" in out

def test_cli_find_move_subcommand(tmp_path, capfd):
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    dst.mkdir()
    (src / "test.txt").write_text("hello")

    argv = ["find-move", str(src), str(dst), "-p", "*.txt"]
    rc = main(argv)
    assert rc == 0
    out, err = capfd.readouterr()
    assert "test.txt" in out
    assert "1 file(s) processed." in out
    assert (dst / "test.txt").exists()

def test_legacy_cli(tmp_path, capfd):
    from filesmith.core import main as legacy_main
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    dst.mkdir()
    (src / "legacy.txt").write_text("legacy")

    # legacy_main expects ["copy", origin, destination, pattern]
    argv = ["copy", str(src), str(dst), ".*\\.txt$"]
    rc = legacy_main(argv)
    assert rc == 0
    out, err = capfd.readouterr()
    assert "legacy.txt" in out
    assert (dst / "legacy.txt").exists()

def test_cli_knapsack_subcommand(tmp_path, capfd):
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    dst.mkdir()
    (src / "small.txt").write_text("a" * 10)
    (src / "large.txt").write_text("a" * 100)

    # knapsack copy src dest capacity
    argv = ["knapsack", "copy", str(src), str(dst), "50"]
    rc = main(argv)
    assert rc == 0
    out, err = capfd.readouterr()
    assert "small.txt" in out
    assert "large.txt" not in out
    assert "selected_total_size: 10" in out
    assert (dst / "small.txt").exists()
    assert not (dst / "large.txt").exists()

def test_cli_duplicates_subcommand(tmp_path, capfd):
    src = tmp_path / "src"
    report = tmp_path / "reports" / "duplicates.txt"
    src.mkdir()
    (src / "a.txt").write_text("same")
    (src / "b.txt").write_text("same")
    (src / "unique.txt").write_text("different")

    rc = main(["duplicates", str(src), "--maxdepth", "0", "-o", str(report)])

    assert rc == 0
    out, err = capfd.readouterr()
    assert "duplicate_groups: 1" in out
    assert "duplicate_files: 2" in out
    assert "group\t1\tsha256\t" in out
    assert report.exists()
    assert "duplicate_groups\t1\n" in report.read_text()
