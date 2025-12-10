from pathlib import Path
from filesmith.engine import FindMoveJob


def test_findmovejob_copy(tmp_path: Path):
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    dst.mkdir()

    (src / "a.txt").write_text("aaa")
    (src / "b.txt").write_text("bbb")
    (src / "c.md").write_text("ccc")

    job = FindMoveJob(
        src_root=src,
        dest_root=dst,
        pattern="*.txt",
        recursive=False,
        mode="copy",
    )
    ops = job.run()

    copied = sorted([p.name for _, p in ops])
    assert copied == ["a.txt", "b.txt"]
    assert (dst / "a.txt").exists()
    assert (dst / "b.txt").exists()


def test_findmovejob_move(tmp_path: Path):
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    dst.mkdir()

    f = src / "m.txt"
    f.write_text("hello")

    job = FindMoveJob(src_root=src, dest_root=dst, pattern="*.txt", mode="move")
    job.run()

    assert not f.exists()
    assert (dst / "m.txt").exists()
