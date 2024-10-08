from pathlib import Path

import pygit2
import pytest


@pytest.fixture()
def git_repo_tmp_path(tmp_path: Path) -> Path:
    pygit2.init_repository(tmp_path)
    return tmp_path
