import os
import tempfile
from pathlib import Path
import pytest
from phases.tokenizer.essay.EssayAutoloader import autoLoadPaths  # adjust import to your module path

@pytest.fixture
def temp_dir_with_files():
    # Create a temporary directory with a few files
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        # Create files
        (base / "file1.txt").write_text("hello world")
        (base / "file2.md").write_text("markdown content")
        # Create a subdirectory (should be ignored)
        os.mkdir(base / "subdir")
        (base / "subdir" / "nested.txt").write_text("nested")
        yield base

def test_returns_full_paths(temp_dir_with_files):
    paths = autoLoadPaths(str(temp_dir_with_files))
    # All returned paths should be absolute
    for p in paths:
        assert Path(p).is_absolute()
    # Should contain only the two files, not the subdir
    filenames = [Path(p).name for p in paths]
    assert set(filenames) == {"file1.txt", "file2.md"}

def test_empty_directory(tmp_path):
    paths = autoLoadPaths(str(tmp_path))
    assert paths == []

def test_default_folder(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    src = tmp_path / "src"
    src.mkdir()
    (src / "essay.txt").write_text("essay content")

    paths = autoLoadPaths(str(src))
    assert len(paths) == 1
    assert Path(paths[0]).name == "essay.txt"
