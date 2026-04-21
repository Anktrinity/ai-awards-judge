from pathlib import Path

from ai_awards_judge.planner import build_manifest


def test_build_manifest_discovers_files(tmp_path: Path) -> None:
    (tmp_path / "entry1.txt").write_text("hello", encoding="utf-8")
    (tmp_path / "nested").mkdir()
    (tmp_path / "nested" / "entry2.txt").write_text("world", encoding="utf-8")

    manifest = build_manifest(tmp_path, tmp_path / "outputs")

    assert manifest.discovered_files == ["entry1.txt", "nested/entry2.txt"]
