from collections.abc import Callable
from typing import Protocol, cast

import pytest
from jsonalias import Json

from dbnomics_data_model.storage.adapters.filesystem.model.releases_json import ReleasesJson


class MakeReleasesData(Protocol):
    def __call__(self, releases: list[dict[str, Json]] | None = None) -> dict[str, Json]: ...


@pytest.fixture()
def make_releases_data() -> Callable[[], dict[str, Json]]:
    def _make_releases_data(releases: list[dict[str, Json]] | None = None) -> dict[str, Json]:
        if releases is None:
            releases = [{"code": "2020-04"}, {"code": "2020-10"}]
        return cast(
            dict[str, Json],
            {
                "dataset_releases": [
                    {
                        "dataset_code_prefix": "WEO",
                        "name": "World Economic Outlook",
                        "releases": releases,
                    },
                ],
            },
        )

    return _make_releases_data


def test_valid_releases(make_releases_data: MakeReleasesData) -> None:
    releases_data = make_releases_data()
    ReleasesJson.parse_obj(releases_data)


def test_invalid_release(make_releases_data: MakeReleasesData, invalid_release_code: str) -> None:
    releases_data = make_releases_data([{"code": invalid_release_code}])
    ReleasesJson.parse_obj(releases_data)
