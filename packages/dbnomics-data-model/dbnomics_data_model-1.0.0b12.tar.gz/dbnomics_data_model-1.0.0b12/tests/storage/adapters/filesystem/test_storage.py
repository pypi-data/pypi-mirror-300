from glob import glob
from pathlib import Path

import pytest
from jsonalias import Json

from dbnomics_data_model.errors import reraise_first_error
from dbnomics_data_model.model import (
    Category,
    CategoryTree,
    DatasetMetadata,
    DatasetReference,
    Observation,
    ProviderMetadata,
    Series,
    SeriesMetadata,
)
from dbnomics_data_model.storage.adapters.filesystem.file_system_storage import FileSystemStorage
from dbnomics_data_model.storage.adapters.filesystem.file_utils import (
    load_json_file,
    parse_json_bytes,
    save_json_file,
    save_jsonl_file,
    serialize_json_line,
)
from dbnomics_data_model.storage.adapters.filesystem.model import TsvSeriesJson
from dbnomics_data_model.storage.adapters.filesystem.variants.tsv.tsv_utils import iter_tsv_observations, save_tsv_file
from dbnomics_data_model.storage.errors import (
    DatasetMetadataLoadError,
    DatasetNotFound,
    ProviderMetadataLoadError,
    SeriesLoadError,
    StorageError,
)

from .file_utils import load_jsonl_file_as_array


@pytest.fixture()
def category_tree_json() -> Json:
    return [
        {
            "code": "C1",
            "children": [
                {
                    "code": "C1.1",
                    "children": [
                        {"code": "D1"},
                        {"code": "D2"},
                    ],
                },
            ],
        },
        {"code": "D0"},
    ]


@pytest.fixture()
def dataset_json() -> Json:
    return {"code": "D1"}


@pytest.fixture()
def provider_json() -> Json:
    return {"code": "P1", "website": "https://example.com/"}


@pytest.fixture()
def series_jsonl() -> list[dict[str, Json]]:
    return [
        {"code": "S1", "observations": [["PERIOD", "VALUE"], ["2020", 1], ["2021", 2]]},
        {"code": "S2", "observations": [["PERIOD", "VALUE"], ["2010", 1.1], ["2011", 2.1]]},
    ]


def test_get_dataset_count_empty_dir(tmp_path: Path) -> None:
    (tmp_path / "D1").mkdir()
    storage = FileSystemStorage(tmp_path)
    dataset_count = storage.get_dataset_count()
    assert dataset_count == 0


def test_load_category_tree(tmp_path: Path, category_tree_json: Json) -> None:
    save_json_file(tmp_path / "category_tree.json", category_tree_json)
    storage = FileSystemStorage(tmp_path)
    category_tree = storage.load_category_tree()
    assert category_tree is not None
    assert category_tree.children[0].code == "C1"
    assert isinstance(category_tree.children[0], Category)
    assert isinstance(category_tree.children[0].children[0], Category)
    assert category_tree.children[0].children[0].code == "C1.1"
    assert category_tree.children[1].code == "D0"


def test_load_dataset_metadata(tmp_path: Path, dataset_json: Json) -> None:
    (tmp_path / "D1").mkdir()
    save_json_file(tmp_path / "D1" / "dataset.json", dataset_json)
    storage = FileSystemStorage(tmp_path)
    dataset_metadata = storage.load_dataset_metadata("D1")
    assert dataset_metadata.code == "D1"


def test_load_dataset_metadata_empty_dir(tmp_path: Path) -> None:
    (tmp_path / "D1").mkdir()
    storage = FileSystemStorage(tmp_path)
    with pytest.raises(DatasetMetadataLoadError):
        storage.load_dataset_metadata("D1")


def test_load_dataset_metadata_not_found(tmp_path: Path) -> None:
    storage = FileSystemStorage(tmp_path)
    with pytest.raises(DatasetMetadataLoadError):
        storage.load_dataset_metadata("D1")


def test_load_dataset_metadata_parse_error(tmp_path: Path) -> None:
    (tmp_path / "D1").mkdir()
    (tmp_path / "D1" / "dataset.json").write_text("{")
    storage = FileSystemStorage(tmp_path)
    with pytest.raises(DatasetMetadataLoadError):
        storage.load_dataset_metadata("D1")


def test_load_provider_metadata(tmp_path: Path, provider_json: Json) -> None:
    save_json_file(tmp_path / "provider.json", provider_json)
    storage = FileSystemStorage(tmp_path)
    provider_metadata = storage.load_provider_metadata()
    assert provider_metadata.code == "P1"
    assert provider_metadata.website == "https://example.com/"


def test_load_provider_metadata_not_found(tmp_path: Path) -> None:
    storage = FileSystemStorage(tmp_path)
    with pytest.raises(ProviderMetadataLoadError):
        storage.load_provider_metadata()


def test_load_provider_metadata_parse_error(tmp_path: Path) -> None:
    (tmp_path / "provider.json").write_text("{")
    storage = FileSystemStorage(tmp_path)
    with pytest.raises(ProviderMetadataLoadError):
        storage.load_provider_metadata()


def test_iter_dataset_codes_no_dataset(tmp_path: Path) -> None:
    storage = FileSystemStorage(tmp_path)
    dataset_codes = list(storage.iter_dataset_codes())
    assert len(dataset_codes) == 0


def test_iter_dataset_codes_dataset_dir(tmp_path: Path, dataset_json: Json) -> None:
    (tmp_path / "D1").mkdir()
    save_json_file(tmp_path / "D1" / "dataset.json", dataset_json)
    storage = FileSystemStorage(tmp_path)
    dataset_codes = list(storage.iter_dataset_codes())
    assert len(dataset_codes) == 1
    assert dataset_codes[0] == "D1"


def test_iter_dataset_codes_empty_dir(tmp_path: Path) -> None:
    (tmp_path / "D1").mkdir()
    storage = FileSystemStorage(tmp_path)
    with pytest.raises(StorageError):
        list(storage.iter_dataset_codes())


def test_iter_dataset_codes_on_error_yield(tmp_path: Path) -> None:
    (tmp_path / "D1").mkdir()
    storage = FileSystemStorage(tmp_path)
    result = list(storage.iter_dataset_codes())
    assert isinstance(result[0], StorageError)


def test_iter_dataset_series_jsonl_no_dimensions(
    tmp_path: Path,
    dataset_json: Json,
    series_jsonl: list[dict[str, Json]],
) -> None:
    (tmp_path / "D1").mkdir()
    save_json_file(tmp_path / "D1" / "dataset.json", dataset_json)
    save_jsonl_file(tmp_path / "D1" / "series.jsonl", series_jsonl)
    storage = FileSystemStorage(tmp_path)
    series = list(reraise_first_error(storage.iter_dataset_series("D1"), SeriesLoadError))
    assert len(series) == 2
    assert series[0].metadata.code == "S1"
    assert series[0].metadata.dimensions == {}
    assert series[0].observations == [
        Observation(period="2020", value=1),
        Observation(period="2021", value=2),
    ]
    assert series[1].metadata.code == "S2"
    assert series[1].metadata.dimensions == {}
    assert series[1].observations == [
        Observation(period="2010", value=1.1),
        Observation(period="2011", value=2.1),
    ]


def test_iter_dataset_series_jsonl_exclude_observations(
    tmp_path: Path,
    dataset_json: Json,
    series_jsonl: list[dict[str, Json]],
) -> None:
    (tmp_path / "D1").mkdir()
    save_json_file(tmp_path / "D1" / "dataset.json", dataset_json)
    save_jsonl_file(tmp_path / "D1" / "series.jsonl", series_jsonl)
    storage = FileSystemStorage(tmp_path)
    series = list(reraise_first_error(storage.iter_dataset_series("D1", with_observations=False), SeriesLoadError))
    assert len(series) == 2
    assert series[0].metadata.code == "S1"
    assert len(series[0].observations) == 0


def test_iter_dataset_series_jsonl_dimensions_as_dict(tmp_path: Path) -> None:
    (tmp_path / "D1").mkdir()
    dataset_json: Json = {
        "code": "D1",
        "dimensions_codes_order": ["FREQ"],
        "dimensions_labels": {"FREQ": "Frequency"},
        "dimensions_values_labels": {"FREQ": {"A": "Annual"}},
    }
    save_json_file(tmp_path / "D1" / "dataset.json", dataset_json)
    series_jsonl: list[dict[str, Json]] = [
        {"code": "S1", "dimensions": {"FREQ": "A"}, "observations": [["PERIOD", "VALUE"], ["2020", 1], ["2021", 2]]},
    ]
    save_jsonl_file(tmp_path / "D1" / "series.jsonl", series_jsonl)
    storage = FileSystemStorage(tmp_path)
    series = list(reraise_first_error(storage.iter_dataset_series("D1"), SeriesLoadError))
    assert len(series) == 1
    assert series[0].metadata.code == "S1"
    assert series[0].metadata.dimensions == {"FREQ": "A"}
    assert series[0].observations == [
        Observation(period="2020", value=1),
        Observation(period="2021", value=2),
    ]


def test_iter_dataset_series_jsonl_dimensions_as_list(tmp_path: Path) -> None:
    (tmp_path / "D1").mkdir()
    dataset_json: Json = {
        "code": "D1",
        "dimensions_codes_order": ["FREQ"],
        "dimensions_labels": {"FREQ": "Frequency"},
        "dimensions_values_labels": {"FREQ": {"A": "Annual"}},
    }
    save_json_file(tmp_path / "D1" / "dataset.json", dataset_json)
    series_jsonl: list[dict[str, Json]] = [
        {"code": "S1", "dimensions": ["A"], "observations": [["PERIOD", "VALUE"], ["2020", 1], ["2021", 2]]},
    ]
    save_jsonl_file(tmp_path / "D1" / "series.jsonl", series_jsonl)
    storage = FileSystemStorage(tmp_path)
    series = list(reraise_first_error(storage.iter_dataset_series("D1"), SeriesLoadError))
    assert len(series) == 1
    assert series[0].metadata.code == "S1"
    assert series[0].metadata.dimensions == {"FREQ": "A"}
    assert series[0].observations == [
        Observation(period="2020", value=1),
        Observation(period="2021", value=2),
    ]


def test_iter_dataset_series_tsv_no_dimensions(tmp_path: Path) -> None:
    (tmp_path / "D1").mkdir()
    dataset_json: Json = {
        "code": "D1",
        "series": [{"code": "S1", "notes": ["line 1", "line 2"]}],
    }
    save_json_file(tmp_path / "D1" / "dataset.json", dataset_json)
    save_tsv_file(tmp_path / "D1" / "S1.tsv", [Observation(period="2000", value=1.1)])

    storage = FileSystemStorage(tmp_path)
    series = list(reraise_first_error(storage.iter_dataset_series("D1"), SeriesLoadError))
    assert len(series) == 1
    assert series[0].metadata.code == "S1"
    assert series[0].metadata.dimensions == {}
    assert series[0].metadata.notes == "line 1\nline 2"
    assert series[0].observations == [Observation(period="2000", value=1.1)]


def test_iter_dataset_series_tsv_dimensions_as_dict(tmp_path: Path) -> None:
    (tmp_path / "D1").mkdir()
    dataset_json: Json = {
        "code": "D1",
        "dimensions_codes_order": ["FREQ"],
        "dimensions_labels": {"FREQ": "Frequency"},
        "dimensions_values_labels": {"FREQ": {"A": "Annual"}},
        "series": [{"code": "S1", "dimensions": {"FREQ": "A"}}],
    }
    save_json_file(tmp_path / "D1" / "dataset.json", dataset_json)
    save_tsv_file(tmp_path / "D1" / "S1.tsv", [Observation(period="2000", value=1.1)])

    storage = FileSystemStorage(tmp_path)
    series = list(reraise_first_error(storage.iter_dataset_series("D1"), SeriesLoadError))
    assert len(series) == 1
    assert series[0].metadata.code == "S1"
    assert series[0].metadata.dimensions == {"FREQ": "A"}
    assert series[0].observations == [Observation(period="2000", value=1.1)]


def test_iter_dataset_series_tsv_dimensions_as_list(tmp_path: Path) -> None:
    (tmp_path / "D1").mkdir()
    dataset_json: Json = {
        "code": "D1",
        "dimensions_codes_order": ["FREQ"],
        "dimensions_labels": {"FREQ": "Frequency"},
        "dimensions_values_labels": {"FREQ": {"A": "Annual"}},
        "series": [{"code": "S1", "dimensions": ["A"]}],
    }
    save_json_file(tmp_path / "D1" / "dataset.json", dataset_json)
    save_tsv_file(tmp_path / "D1" / "S1.tsv", [Observation(period="2000", value=1.1)])

    storage = FileSystemStorage(tmp_path)
    series = list(reraise_first_error(storage.iter_dataset_series("D1"), SeriesLoadError))
    assert len(series) == 1
    assert series[0].metadata.code == "S1"
    assert series[0].metadata.dimensions == {"FREQ": "A"}
    assert series[0].observations == [Observation(period="2000", value=1.1)]


def test_iter_series_jsonl_variant(tmp_path: Path) -> None:
    (tmp_path / "D1").mkdir()
    dataset_json: Json = {"code": "D1"}
    save_json_file(tmp_path / "D1" / "dataset.json", dataset_json)
    series_jsonl: list[dict[str, Json]] = [
        {"code": "S1", "observations": [["PERIOD", "VALUE"], ["2020", 1], ["2021", 2]]},
        {"code": "S2", "observations": [["PERIOD", "VALUE"], ["2020", 3], ["2021", 4]]},
    ]
    save_jsonl_file(tmp_path / "D1" / "series.jsonl", series_jsonl)
    storage = FileSystemStorage(tmp_path)
    dataset_json_2 = storage.load_dataset_json("D1", storage_variant="jsonl")
    series_and_offsets = list(
        reraise_first_error(
            storage.iter_series_jsonl_variant(
                "D1",
                dataset_json=dataset_json_2,
                with_observations=False,
            ),
            SeriesLoadError,
        )
    )
    assert len(series_and_offsets) == 2
    series1, offset1 = series_and_offsets[0]
    assert series1.metadata.code == "S1"
    assert offset1 == 0
    series2, offset2 = series_and_offsets[1]
    assert series2.metadata.code == "S2"
    assert offset2 == len(serialize_json_line(series_jsonl[0])) + len("\n")


def test_merge_dataset(tmp_path: Path) -> None:
    storage1_dir = tmp_path / "storage1"
    storage1_dir.mkdir()
    storage2_dir = tmp_path / "storage2"
    storage2_dir.mkdir()

    storage1 = FileSystemStorage(storage1_dir)
    dataset_metadata = DatasetMetadata(id=("P1", "D1"))
    storage1.save_dataset_metadata(dataset_metadata)
    storage1.save_dataset_series(
        [
            Series(metadata=SeriesMetadata(id=("P1", "D1", "S1")), observations=[Observation(period="2014", value=1)]),
            Series(metadata=SeriesMetadata(id=("P1", "D1", "S2")), observations=[Observation(period="2020", value=10)]),
        ],
        dataset_metadata=dataset_metadata,
    )

    storage2 = FileSystemStorage(storage2_dir)
    dataset_metadata = DatasetMetadata(id=("P1", "D1"))
    storage2.save_dataset_metadata(dataset_metadata)
    storage2.save_dataset_series(
        [
            Series(
                metadata=SeriesMetadata(id=("P1", "D1", "S1")), observations=[Observation(period="2014", value=1.1)]
            ),
            Series(
                metadata=SeriesMetadata(id=("P1", "D1", "S3")), observations=[Observation(period="2020", value=10.1)]
            ),
        ],
        dataset_metadata=dataset_metadata,
    )

    storage1.merge_dataset("D1", storage2)

    merged_dataset_series = list(reraise_first_error(storage1.iter_dataset_series("D1"), SeriesLoadError))
    assert len(merged_dataset_series) == 3
    assert merged_dataset_series[0].metadata.code == "S1"
    assert len(merged_dataset_series[0].observations) == 1
    assert merged_dataset_series[0].observations[0].period == "2014"
    assert merged_dataset_series[0].observations[0].value == 1.1
    assert len(merged_dataset_series[1].observations) == 1
    assert merged_dataset_series[1].metadata.code == "S2"
    assert merged_dataset_series[1].observations[0].period == "2020"
    assert merged_dataset_series[1].observations[0].value == 10
    assert len(merged_dataset_series[2].observations) == 1
    assert merged_dataset_series[2].metadata.code == "S3"
    assert merged_dataset_series[2].observations[0].period == "2020"
    assert merged_dataset_series[2].observations[0].value == 10.1


def test_merge_dataset_tsv(tmp_path: Path) -> None:
    storage1_dir = tmp_path / "storage1"
    storage1_dir.mkdir()
    storage2_dir = tmp_path / "storage2"
    storage2_dir.mkdir()

    storage1 = FileSystemStorage(storage1_dir, storage_variant="tsv")
    dataset_metadata = DatasetMetadata(id=("P1", "D1"))
    storage1.save_dataset_metadata(dataset_metadata)
    storage1.save_dataset_series(
        [
            Series(metadata=SeriesMetadata(id=("P1", "D1", "S1")), observations=[Observation(period="2014", value=1)]),
            Series(metadata=SeriesMetadata(id=("P1", "D1", "S2")), observations=[Observation(period="2020", value=10)]),
        ],
        dataset_metadata=dataset_metadata,
    )

    storage2 = FileSystemStorage(storage2_dir, storage_variant="tsv")
    dataset_metadata = DatasetMetadata(id=("P1", "D1"))
    storage2.save_dataset_metadata(dataset_metadata)
    storage2.save_dataset_series(
        [
            Series(
                metadata=SeriesMetadata(id=("P1", "D1", "S1")), observations=[Observation(period="2014", value=1.1)]
            ),
            Series(
                metadata=SeriesMetadata(id=("P1", "D1", "S3")), observations=[Observation(period="2020", value=10.1)]
            ),
        ],
        dataset_metadata=dataset_metadata,
    )

    storage1.merge_dataset("D1", storage2)

    assert storage1.detect_dataset_storage_variant("D1") == "tsv"
    assert glob(str(storage1_dir / "D1" / "series.jsonl")) == []


def test_merge_dataset_tsv_by_detecting(tmp_path: Path) -> None:
    storage1_dir = tmp_path / "storage1"
    storage1_dir.mkdir()
    storage2_dir = tmp_path / "storage2"
    storage2_dir.mkdir()

    storage1 = FileSystemStorage(storage1_dir)
    (storage1_dir / "D1").mkdir()
    dataset_json_1: Json = {"code": "D1", "series": [{"code": "S1"}]}
    save_json_file(storage1_dir / "D1" / "dataset.json", dataset_json_1)
    save_tsv_file(storage1_dir / "D1" / "S1.tsv", [Observation(period="2000", value=1.1)])

    storage2 = FileSystemStorage(storage2_dir)
    (storage2_dir / "D1").mkdir()
    dataset_json_2: Json = {"code": "D1", "series": [{"code": "S2"}]}
    save_json_file(storage2_dir / "D1" / "dataset.json", dataset_json_2)
    save_tsv_file(storage2_dir / "D1" / "S2.tsv", [Observation(period="2001", value=2.1)])

    storage1.merge_dataset("D1", storage2)

    assert storage1.detect_dataset_storage_variant("D1") == "tsv"
    assert glob(str(storage1_dir / "D1" / "series.jsonl")) == []


def test_replace_dataset_tsv(tmp_path: Path) -> None:
    storage1_dir = tmp_path / "storage1"
    storage1_dir.mkdir()
    storage2_dir = tmp_path / "storage2"
    storage2_dir.mkdir()

    (storage2_dir / "D1").mkdir()
    dataset_json: Json = {"code": "D1", "series": [{"code": "S1"}]}
    save_json_file(storage2_dir / "D1" / "dataset.json", dataset_json)
    save_tsv_file(storage2_dir / "D1" / "S1.tsv", [Observation(period="2000", value=1.1)])

    storage1 = FileSystemStorage(storage1_dir)
    storage2 = FileSystemStorage(storage2_dir)

    storage1.replace_dataset("D1", storage2)

    assert storage1.get_storage_variant("D1") == "tsv"


def test_replace_provider_metadata(tmp_path: Path) -> None:
    storage1_dir = tmp_path / "storage1"
    storage1_dir.mkdir()
    storage2_dir = tmp_path / "storage2"
    storage2_dir.mkdir()

    storage1 = FileSystemStorage(storage1_dir)
    storage1.save_provider_metadata(ProviderMetadata(code="p1", website="https://exampl.com/"))

    storage2 = FileSystemStorage(storage2_dir)
    storage2.save_provider_metadata(ProviderMetadata(code="P1", website="https://example.com/"))

    storage1.replace_provider_metadata(storage2)

    provider_metadata = storage1.load_provider_metadata()
    assert provider_metadata.code == "P1"
    assert provider_metadata.website == "https://example.com/"


def test_update_with_empty_storage(tmp_path: Path) -> None:
    storage1_dir = tmp_path / "storage1"
    storage1_dir.mkdir()
    storage2_dir = tmp_path / "storage2"
    storage2_dir.mkdir()

    storage1 = FileSystemStorage(storage1_dir)

    storage2 = FileSystemStorage(storage2_dir)
    storage2.save_provider_metadata(ProviderMetadata(code="P1", website="https://example.com/"))
    dataset_metadata = DatasetMetadata(id=("P1", "D1"))
    storage2.save_dataset_metadata(dataset_metadata)
    storage2.save_dataset_series(
        [
            Series(metadata=SeriesMetadata(id=("P1", "D1", "S1")), observations=[Observation(period="2014", value=1)]),
        ],
        dataset_metadata=dataset_metadata,
    )

    storage1.update_provider(storage2)

    provider_metadata = storage1.load_provider_metadata()
    assert provider_metadata.code == "P1"
    dataset_metadata = storage1.load_dataset_metadata("D1")
    assert dataset_metadata.code == "D1"
    series = list(
        reraise_first_error(
            storage1.iter_dataset_series("D1", with_observations=True, series_codes={"S1"}), SeriesLoadError
        )
    )
    assert len(series) == 1
    assert series[0].metadata.code == "S1"
    assert len(series[0].observations) == 1
    assert series[0].observations[0].period == "2014"
    assert series[0].observations[0].value == 1


def test_save_provider_metadata(tmp_path: Path) -> None:
    storage = FileSystemStorage(tmp_path)
    provider_metadata = ProviderMetadata(code="P2", website="https://p2.com/")
    storage.save_provider_metadata(provider_metadata)
    provider_json = load_json_file(tmp_path / "provider.json")
    assert isinstance(provider_json, dict)
    assert provider_json["code"] == "P2"
    assert provider_json["website"] == "https://p2.com/"


def test_save_category_tree(tmp_path: Path) -> None:
    storage = FileSystemStorage(tmp_path)
    category_tree = CategoryTree(
        children=[
            DatasetReference(code="foo"),
            Category(code="c1", children=[DatasetReference(code="c1d1")]),
        ],
    )
    storage.save_category_tree(category_tree)
    category_tree_json = load_json_file(tmp_path / "category_tree.json")
    assert isinstance(category_tree_json, list)
    assert len(category_tree_json) == 2
    assert isinstance(category_tree_json[0], dict)
    assert category_tree_json[0]["code"] == "foo"
    assert isinstance(category_tree_json[1], dict)
    assert category_tree_json[1]["code"] == "c1"
    assert isinstance(category_tree_json[1]["children"], list)
    assert isinstance(category_tree_json[1]["children"][0], dict)
    assert category_tree_json[1]["children"][0]["code"] == "c1d1"


def test_save_dataset_metadata(tmp_path: Path) -> None:
    storage = FileSystemStorage(tmp_path)
    dataset_metadata = DatasetMetadata(id=("P1", "D2"))
    storage.save_dataset_metadata(dataset_metadata)
    provider_json = load_json_file(tmp_path / "D2" / "dataset.json")
    assert isinstance(provider_json, dict)
    assert provider_json["code"] == "D2"


def test_save_dataset_series_detect_variant(tmp_path: Path, dataset_json: Json) -> None:
    (tmp_path / "D1").mkdir()
    save_json_file(tmp_path / "D1" / "dataset.json", dataset_json)

    storage = FileSystemStorage(tmp_path)

    assert storage.storage_variant == "detect"
    assert storage.detect_dataset_storage_variant("D1") is None

    dataset_metadata = DatasetMetadata(id=("P1", "D1"))
    storage.save_dataset_series([], dataset_metadata=dataset_metadata)
    assert storage.detect_dataset_storage_variant("D1") == storage.default_storage_variant
    assert storage.get_storage_variant("D1") == storage.default_storage_variant

    series = [
        Series(metadata=SeriesMetadata(id=("P1", "D1", "S1")), observations=[Observation(period="2014", value=1)]),
        Series(
            metadata=SeriesMetadata(id=("P1", "D1", "S2"), notes="This is a note"),
            observations=[Observation(period="2015", value=2)],
        ),
    ]
    storage.save_dataset_series(series, dataset_metadata=dataset_metadata)
    assert storage.detect_dataset_storage_variant("D1") == "jsonl"
    assert storage.get_storage_variant("D1") == "jsonl"

    assert glob(str(tmp_path / "D1" / "*.tsv")) == []


def test_save_dataset_series_jsonl_variant(tmp_path: Path, dataset_json: Json) -> None:
    (tmp_path / "D1").mkdir()
    save_json_file(tmp_path / "D1" / "dataset.json", dataset_json)

    storage = FileSystemStorage(tmp_path, storage_variant="jsonl")
    assert storage.storage_variant == "jsonl"

    dataset_metadata = DatasetMetadata(id=("P1", "D1"))
    series = [
        Series(metadata=SeriesMetadata(id=("P1", "D1", "S1")), observations=[Observation(period="2014", value=1)]),
        Series(
            metadata=SeriesMetadata(id=("P1", "D1", "S2"), notes="This is a note"),
            observations=[Observation(period="2015", value=2)],
        ),
    ]
    storage.save_dataset_series(series, dataset_metadata=dataset_metadata)
    assert storage.detect_dataset_storage_variant("D1") == "jsonl"
    assert storage.get_storage_variant("D1") == "jsonl"

    with (tmp_path / "D1" / "series.jsonl").open("rb") as fp:
        for line_index, line in enumerate(fp):
            series_json = parse_json_bytes(line)
            assert isinstance(series_json, dict)
            assert series_json["code"] == series[line_index].metadata.code
            assert isinstance(series_json["observations"], list)
            assert isinstance(series_json["observations"][1], list)
            assert series_json["observations"][1][0] == series[line_index].observations[0].period
            assert series_json["observations"][1][1] == series[line_index].observations[0].value
            if series_json["code"] == "S2":
                assert isinstance(series_json["notes"], list)
                assert series_json["notes"][0] == "This is a note"

    assert glob(str(tmp_path / "D1" / "*.tsv")) == []


def test_save_dataset_series_tsv_variant(tmp_path: Path) -> None:
    storage = FileSystemStorage(tmp_path, storage_variant="tsv")
    assert storage.storage_variant == "tsv"

    dataset_metadata = DatasetMetadata(id=("P1", "D1"))
    storage.save_dataset_metadata(dataset_metadata)

    series = [
        Series(metadata=SeriesMetadata(id=("P1", "D1", "S1")), observations=[Observation(period="2014", value=1)]),
        Series(
            metadata=SeriesMetadata(id=("P1", "D1", "S2"), notes="This is a note"),
            observations=[Observation(period="2015", value=2)],
        ),
    ]
    storage.save_dataset_series(series, dataset_metadata=dataset_metadata)
    assert storage.detect_dataset_storage_variant("D1") == "tsv"
    assert storage.get_storage_variant("D1") == "tsv"

    tsv_observations = (tmp_path / "D1" / "S1.tsv").read_text()
    observations = list(iter_tsv_observations(tsv_observations))
    assert observations[0].period == "2014"
    assert observations[0].value == 1

    assert glob(str(tmp_path / "D1" / "series.jsonl")) == []


def test_save_dataset_series_tsv_variant_before_saving_dataset_metadata(tmp_path: Path) -> None:
    storage = FileSystemStorage(tmp_path, storage_variant="tsv")
    assert storage.storage_variant == "tsv"

    dataset_metadata = DatasetMetadata(id=("P1", "D1"))
    series = [
        Series(metadata=SeriesMetadata(id=("P1", "D1", "S1")), observations=[Observation(period="2014", value=1)]),
        Series(
            metadata=SeriesMetadata(id=("P1", "D1", "S2"), notes="This is a note"),
            observations=[Observation(period="2015", value=2)],
        ),
    ]
    storage.save_dataset_series(series, dataset_metadata=dataset_metadata)

    tsv_observations = (tmp_path / "D1" / "S1.tsv").read_text()
    observations = list(iter_tsv_observations(tsv_observations))
    assert observations[0].period == "2014"
    assert observations[0].value == 1

    assert glob(str(tmp_path / "D1" / "series.jsonl")) == []


def test_delete(tmp_path: Path) -> None:
    storage = FileSystemStorage(tmp_path)
    assert tmp_path.is_dir()
    storage.delete_provider()
    assert not tmp_path.exists()


def test_delete_non_existent_dataset_missing_ko(tmp_path: Path) -> None:
    storage = FileSystemStorage(tmp_path)

    with pytest.raises(DatasetNotFound):
        storage.delete_dataset("D1")


def test_delete_non_existent_dataset_missing_ok(tmp_path: Path) -> None:
    storage = FileSystemStorage(tmp_path)

    storage.delete_dataset("D1", missing_ok=True)


def test_context_manager_noop(tmp_path: Path) -> None:
    with FileSystemStorage(tmp_path):
        pass


def test_without_context_manager_and_append_mode(tmp_path: Path) -> None:
    storage = FileSystemStorage(tmp_path)
    dataset_metadata = DatasetMetadata(id=("P1", "D1"))
    s1 = Series(
        metadata=SeriesMetadata(id=("P1", "D1", "S1")),
        observations=[Observation(period="2020", value=0), Observation(period="2021", value=1)],
    )
    with pytest.raises(RuntimeError):
        storage.save_dataset_series(s1, dataset_metadata=dataset_metadata, mode="append")


def test_context_manager_interleave_writing_different_datasets(tmp_path: Path) -> None:
    d1_metadata = DatasetMetadata(id=("P1", "D1"))
    d2_metadata = DatasetMetadata(id=("P1", "D2"))
    s1 = Series(
        metadata=SeriesMetadata(id=("P1", "D1", "S1")),
        observations=[Observation(period="2020", value=0), Observation(period="2021", value=1)],
    )
    s2 = Series(
        metadata=SeriesMetadata(id=("P1", "D1", "S2")),
        observations=[Observation(period="2020", value=0), Observation(period="2021", value=1)],
    )
    s3 = Series(
        metadata=SeriesMetadata(id=("P1", "D1", "S3")),
        observations=[Observation(period="2020", value=0), Observation(period="2021", value=1)],
    )
    with FileSystemStorage(tmp_path) as storage:
        storage.save_dataset_series(s1, dataset_metadata=d1_metadata, mode="append")
        storage.save_dataset_series(s2, dataset_metadata=d2_metadata, mode="append")
        storage.save_dataset_series(s3, dataset_metadata=d1_metadata, mode="append")


def test_multiple_storage_instances_with_append_mode(tmp_path: Path) -> None:
    dataset_metadata = DatasetMetadata(id=("P1", "D1"))
    series_list = [
        Series(metadata=SeriesMetadata(id=("P1", "D1", "S1")), observations=[Observation(period="2000", value=1)]),
        Series(metadata=SeriesMetadata(id=("P1", "D1", "S2")), observations=[Observation(period="2000", value=1)]),
    ]
    for series in series_list:
        with FileSystemStorage(tmp_path) as storage:
            storage.save_dataset_series(series, dataset_metadata=dataset_metadata, mode="append")
    series_json = load_jsonl_file_as_array(tmp_path / "D1" / "series.jsonl")
    assert isinstance(series_json, list)
    assert isinstance(series_json[0], dict)
    assert series_json[0]["code"] == "S1"
    assert isinstance(series_json[1], dict)
    assert series_json[1]["code"] == "S2"


def test_series_metadata_is_kept_when_saving_dataset_metadata_with_tsv_variant(tmp_path: Path) -> None:
    storage = FileSystemStorage(tmp_path, storage_variant="tsv")

    dataset_metadata = DatasetMetadata(id=("P1", "D1"))
    storage.save_dataset_metadata(dataset_metadata)

    series = Series(metadata=SeriesMetadata(id=("P1", "D1", "S1")), observations=[])
    storage.save_dataset_series(series, dataset_metadata=dataset_metadata)

    dataset_metadata.name = "Dataset 1"
    storage.save_dataset_metadata(dataset_metadata)

    dataset_json = storage.load_dataset_json("D1", storage_variant="tsv")
    assert dataset_json.code == "D1"
    assert dataset_json.name == "Dataset 1"
    assert dataset_json.series == [TsvSeriesJson(code="S1")]
