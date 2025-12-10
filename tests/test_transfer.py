from pathlib import Path
from filesmith.transfer import transfer_files


def test_transfer_copy_basic(tmp_path: Path):
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    dst.mkdir()

    file_a = src / "a.txt"
    file_a.write_text("hello")

    ops = transfer_files([file_a], dst, mode="copy", dry_run=False)

    assert (dst / "a.txt").exists()
    assert (dst / "a.txt").read_text() == "hello"
    assert ops == [(file_a, dst / "a.txt")]


def test_transfer_move_basic(tmp_path: Path):
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    dst.mkdir()

    f = src / "m.txt"
    f.write_text("move me")

    transfer_files([f], dst, mode="move")

    assert not f.exists()
    assert (dst / "m.txt").exists()


def test_transfer_conflict_skip(tmp_path: Path):
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    dst.mkdir()

    f = src / "a.txt"
    f.write_text("hello")

    # already exists in destination
    (dst / "a.txt").write_text("existing")

    ops = transfer_files([f], dst, mode="copy", on_conflict="skip")

    assert ops == []  # skipped
    assert (dst / "a.txt").read_text() == "existing"


def test_transfer_conflict_overwrite(tmp_path: Path):
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    dst.mkdir()

    f = src / "a.txt"
    f.write_text("new content")

    (dst / "a.txt").write_text("old content")

    transfer_files([f], dst, mode="copy", on_conflict="overwrite")

    assert (dst / "a.txt").read_text() == "new content"
