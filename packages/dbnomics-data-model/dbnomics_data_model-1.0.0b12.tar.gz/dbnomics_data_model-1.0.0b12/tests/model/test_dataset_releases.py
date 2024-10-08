import pytest

from dbnomics_data_model.model import DatasetRelease, DatasetReleases, DatasetReleasesItem
from dbnomics_data_model.model.validation.dataset_releases import validate_dataset_release_metadata
from dbnomics_data_model.storage.adapters.filesystem.model.releases_json import ReleasesJson


def test_valid_releases() -> None:
    dataset_release_metadata = DatasetReleases(
        dataset_releases=[
            DatasetReleasesItem(
                bare_dataset_code="D1",
                releases=[DatasetRelease(code="R1")],
            )
        ]
    )
    validate_dataset_release_metadata(dataset_release_metadata)


def test_invalid_releases(make_releases_data: MakeReleasesData, invalid_release_code: str) -> None:
    # TODO
    releases_data = make_releases_data([{"code": invalid_release_code}])
    with pytest.raises(ValidationError):
        ReleasesJson.parse_obj(releases_data)


def test_find_dataset_releases_item(make_releases_data: MakeReleasesData) -> None:
    releases_data = make_releases_data()
    releases_json = ReleasesJson.parse_obj(releases_data)

    dataset_releases_item = releases_json.find_dataset_releases_item("WEO")
    assert dataset_releases_item is not None
    assert dataset_releases_item.dataset_code_prefix == "WEO"

    dataset_releases_item = releases_json.find_dataset_releases_item("foo")
    assert dataset_releases_item is None


def test_resolve_release_code_with_latest(make_releases_data: MakeReleasesData) -> None:
    releases_data = make_releases_data()
    releases = ReleasesJson.parse_obj(releases_data)

    resolved_dataset_code = releases.resolve_release_code("WEO:latest")
    assert resolved_dataset_code == "WEO:2020-10"


def test_resolve_release_code_without_release_code(make_releases_data: MakeReleasesData) -> None:
    releases_data = make_releases_data()
    releases = ReleasesJson.parse_obj(releases_data)

    resolved_dataset_code = releases.resolve_release_code("WEO")
    assert resolved_dataset_code == "WEO"


def test_resolve_release_code_with_invalid(make_releases_data: MakeReleasesData, invalid_release_code: str) -> None:
    releases_data = make_releases_data()
    releases = ReleasesJson.parse_obj(releases_data)

    with pytest.raises(ValueError, match=f"Release code {invalid_release_code!r} does not conform to pattern"):
        releases.resolve_release_code(f"WEO:{invalid_release_code}")


def test_merge_releases_empty(make_releases_data: MakeReleasesData) -> None:
    previous_releases_data = make_releases_data()
    previous_releases = ReleasesJson.parse_obj(previous_releases_data)
    releases = DatasetReleases()
    merged_releases = previous_releases.merge(releases)
    assert len(merged_releases.dataset_releases) == len(previous_releases.dataset_releases)
    assert merged_releases.dataset_releases[0].dataset_code_prefix == "WEO"


def test_merge_releases_identical(make_releases_data: MakeReleasesData) -> None:
    previous_releases_data = make_releases_data()
    previous_releases = ReleasesJson.parse_obj(previous_releases_data)
    merged_releases = previous_releases.merge(previous_releases)
    assert len(merged_releases.dataset_releases) == len(previous_releases.dataset_releases)
    assert (
        merged_releases.dataset_releases[0].dataset_code_prefix
        == merged_releases.dataset_releases[0].dataset_code_prefix
    )


def test_merge_releases_new_name_wins(make_releases_data: MakeReleasesData) -> None:
    previous_releases_data = make_releases_data()
    previous_releases = ReleasesJson.parse_obj(previous_releases_data)
    releases = DatasetReleases(
        dataset_releases=[
            DatasetReleasesItem(bare_dataset_code="WEO", name="WEO new name", releases=[]),
        ],
    )
    merged_releases = previous_releases.merge(releases)
    assert merged_releases.dataset_releases[0].name == "WEO new name"


def test_merge_releases_order(make_releases_data: MakeReleasesData) -> None:
    previous_releases_data = make_releases_data()
    previous_releases = ReleasesJson.parse_obj(previous_releases_data)
    releases = DatasetReleases(
        dataset_releases=[
            DatasetReleasesItem(bare_dataset_code="WEO", releases=[DatasetRelease(code="1000")]),
            DatasetReleasesItem(
                bare_dataset_code="AAA",
                releases=[DatasetRelease(code="new")],
            ),
        ],
    )
    merged_releases = previous_releases.merge(releases)
    assert len(merged_releases.dataset_releases) == 2
    assert merged_releases.dataset_releases[0].dataset_code_prefix == "AAA"
    assert merged_releases.dataset_releases[0].releases[0].code == "new"
    assert len(merged_releases.dataset_releases[0].releases) == 1
    assert merged_releases.dataset_releases[1].dataset_code_prefix == "WEO"
    assert len(merged_releases.dataset_releases[1].releases) == 3
    assert merged_releases.dataset_releases[1].releases[0].code == "1000"
