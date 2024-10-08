from pathlib import Path

import pytest
from pygit2 import GIT_FILEMODE_BLOB, IndexEntry, Repository, Signature

from dbnomics_data_model.storage.adapters.filesystem.errors.git_provider_directory_manager import (
    RepositoryDirectoryNotFound,
    RepositoryOpenError,
)
from dbnomics_data_model.storage.adapters.filesystem.git.git_provider_directory_manager import (
    GitProviderDirectoryManager,
)


def test_open_dir_not_exists() -> None:
    with pytest.raises(RepositoryDirectoryNotFound):
        GitProviderDirectoryManager.open("/a/b/c")


def test_open_dir_not_a_repo(tmp_path: Path) -> None:
    with pytest.raises(RepositoryOpenError):
        GitProviderDirectoryManager.open(tmp_path)


def test_open_valid(git_repo_tmp_path: Path) -> None:
    GitProviderDirectoryManager.open(git_repo_tmp_path)


def test_does_commit_change_file_one_commit(git_repo_tmp_path: Path) -> None:
    repo = Repository(git_repo_tmp_path)
    author = Signature("Alice Author", "alice@authors.tld")
    blob_id = repo.create_blob(b"foo")
    entry = IndexEntry("foo.txt", blob_id, GIT_FILEMODE_BLOB)
    repo.index.add(entry)
    tree_id = repo.index.write_tree()
    commit_oid = repo.create_commit("HEAD", author, author, "foo", tree_id, [])

    manager = GitProviderDirectoryManager(repo=repo)

    assert manager.does_commit_change_file("foo.txt")
    assert manager.does_commit_change_file("foo.txt", revision_id="HEAD")
    assert manager.does_commit_change_file("foo.txt", revision_id=commit_oid.hex)


def test_does_commit_change_file_first_commit(git_repo_tmp_path: Path) -> None:
    repo = Repository(git_repo_tmp_path)
    author = Signature("Alice Author", "alice@authors.tld")

    blob_id = repo.create_blob(b"foo")
    entry = IndexEntry("foo.txt", blob_id, GIT_FILEMODE_BLOB)
    repo.index.add(entry)
    tree_id = repo.index.write_tree()
    foo_commit_oid = repo.create_commit("HEAD", author, author, "foo", tree_id, [])

    blob_id = repo.create_blob(b"bar")
    entry = IndexEntry("bar.txt", blob_id, GIT_FILEMODE_BLOB)
    repo.index.add(entry)
    tree_id = repo.index.write_tree()
    bar_commit_oid = repo.create_commit("HEAD", author, author, "bar", tree_id, [foo_commit_oid])

    manager = GitProviderDirectoryManager(repo=repo)

    assert manager.does_commit_change_file("foo.txt", revision_id=foo_commit_oid.hex)
    assert not manager.does_commit_change_file("foo.txt", revision_id=bar_commit_oid.hex)


def test_does_commit_change_file_second_commit(git_repo_tmp_path: Path) -> None:
    repo = Repository(git_repo_tmp_path)
    author = Signature("Alice Author", "alice@authors.tld")

    blob_id = repo.create_blob(b"bar")
    entry = IndexEntry("bar.txt", blob_id, GIT_FILEMODE_BLOB)
    repo.index.add(entry)
    tree_id = repo.index.write_tree()
    bar_commit_oid = repo.create_commit("HEAD", author, author, "bar", tree_id, [])

    blob_id = repo.create_blob(b"foo")
    entry = IndexEntry("foo.txt", blob_id, GIT_FILEMODE_BLOB)
    repo.index.add(entry)
    tree_id = repo.index.write_tree()
    foo_commit_oid = repo.create_commit("HEAD", author, author, "foo", tree_id, [bar_commit_oid])

    manager = GitProviderDirectoryManager(repo=repo)

    assert manager.does_commit_change_file("foo.txt", revision_id=foo_commit_oid.hex)
    assert not manager.does_commit_change_file("foo.txt", revision_id=bar_commit_oid.hex)
