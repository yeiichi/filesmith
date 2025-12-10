from pathlib import Path

from filesmith.cli_findmove import main


def test_cli_findmove_copy_dry_run(tmp_path, capfd):
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    dst.mkdir()

    (src / "a.txt").write_text("aaa")
    (src / "b.md").write_text("bbb")

    argv = [
        str(src),
        str(dst),
        "-p",
        "*.txt",
        "--dry-run",
    ]

    rc = main(argv)
    assert rc == 0

    out, err = capfd.readouterr()

    # should show only a.txt
    assert "a.txt" in out
    assert "b.md" not in out
    assert "1 file(s) processed." in out
    assert err == ""


def test_cli_findmove_move(tmp_path, capfd):
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    dst.mkdir()

    f = src / "m.txt"
    f.write_text("hello")

    argv = [
        str(src),
        str(dst),
        "-p",
        "*.txt",
        "-m",
        "move",
    ]

    rc = main(argv)
    assert rc == 0

    out, err = capfd.readouterr()
    assert "m.txt" in out
    assert "1 file(s) processed." in out
    assert err == ""

    # check filesystem side-effect
    assert not f.exists()
    assert (dst / "m.txt").exists()
