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


def test_v2_distinguishes_empty_file_and_directory(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.touch()
    file_hash = paqpy.hash_source(source, False)
    source.unlink()
    source.mkdir()

    assert file_hash != paqpy.hash_source(source, False)


def test_v2_separates_path_from_content(tmp_path: Path) -> None:
    source = tmp_path / "a"
    source.write_bytes(b"bc")
    first_hash = paqpy.hash_source(tmp_path, False)
    source.unlink()
    (tmp_path / "ab").write_bytes(b"c")

    assert first_hash != paqpy.hash_source(tmp_path, False)


def make_symlink(link: Path, target: Path, is_directory: bool = False) -> None:
    try:
        link.symlink_to(target, target_is_directory=is_directory)
    except (OSError, NotImplementedError) as error:
        pytest.skip(f"Symlinks unavailable: {error}")


@pytest.mark.parametrize("is_directory", [False, True])
@pytest.mark.parametrize("root_link", [False, True])
def test_follow_links_controls_target_hashing(
    tmp_path: Path, is_directory: bool, root_link: bool
) -> None:
    target = tmp_path / "target"
    if is_directory:
        target.mkdir()
        content = target / "content.txt"
    else:
        content = target
    content.write_text("before", encoding="utf-8")
    source = tmp_path / "source"
    source.mkdir()
    link = source / "link"
    make_symlink(link, target, is_directory)
    if root_link:
        source = link

    default_hash = paqpy.hash_source(source, False)
    assert default_hash == paqpy.hash_source(source, False, follow_links=False)
    followed_hash = paqpy.hash_source(source, False, follow_links=True)
    if root_link:
        assert followed_hash == paqpy.hash_source(target, False)

    content.write_text("after", encoding="utf-8")

    assert default_hash == paqpy.hash_source(source, False)
    assert followed_hash != paqpy.hash_source(source, False, True)


def test_following_broken_link_raises_file_not_found(tmp_path: Path) -> None:
    link = tmp_path / "link"
    make_symlink(link, tmp_path / "missing")

    assert_hash(paqpy.hash_source(link, False))
    with pytest.raises(FileNotFoundError, match="failed to traverse source"):
        paqpy.hash_source(link, False, follow_links=True)


def test_following_symlink_cycle_raises_paq_error(tmp_path: Path) -> None:
    make_symlink(tmp_path / "loop", tmp_path, is_directory=True)

    assert_hash(paqpy.hash_source(tmp_path, False))
    with pytest.raises(paqpy.PaqError, match="failed to traverse source"):
        paqpy.hash_source(tmp_path, False, follow_links=True)
