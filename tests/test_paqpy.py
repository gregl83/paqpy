from pathlib import Path

import paqpy
import pytest


def assert_hash(value: str) -> None:
    assert len(value) == 64
    assert all(character in "0123456789abcdef" for character in value)


def test_hashes_file_from_pathlike(tmp_path: Path) -> None:
    source = tmp_path / "source.txt"
    source.write_text("paqpy", encoding="utf-8")

    source_hash = paqpy.hash_source(source, True)

    assert_hash(source_hash)
    assert source_hash == paqpy.hash_source(str(source), True)


def test_ignore_hidden_controls_directory_hash(tmp_path: Path) -> None:
    (tmp_path / "visible.txt").write_text("visible", encoding="utf-8")
    hidden = tmp_path / ".hidden.txt"
    hidden.write_text("hidden", encoding="utf-8")

    ignored_hash = paqpy.hash_source(tmp_path, True)
    included_hash = paqpy.hash_source(tmp_path, False)
    hidden.unlink()

    assert_hash(ignored_hash)
    assert ignored_hash != included_hash
    assert ignored_hash == paqpy.hash_source(tmp_path, True)


def test_missing_source_raises_file_not_found(tmp_path: Path) -> None:
    source = tmp_path / "missing"

    with pytest.raises(FileNotFoundError, match="failed to traverse source"):
        paqpy.hash_source(source, True)


def test_exports_fallback_error() -> None:
    assert issubclass(paqpy.PaqError, Exception)
