from datetime import datetime

import pytest

from dbnomics_data_model.model import DatasetMetadata, SeriesMetadata
from dbnomics_data_model.storage.adapters.filesystem.model import TsvDatasetJson, TsvSeriesJson


def test_instance_is_valid() -> None:
    # Just test that no exception is raised.
    TsvDatasetJson(
        code="d1",
        dimensions_codes_order=["FREQ", "COUNTRY"],
        dimensions_labels={"COUNTRY": "Country", "FREQ": "Frequency"},
        dimensions_values_labels={"COUNTRY": {"FR": "France"}, "FREQ": {"A": "Annual"}},
    )


def test_check_dimensions_labels_keys_valid_when_missing() -> None:
    # Just test that no exception is raised.
    TsvDatasetJson(
        code="d1",
        dimensions_codes_order=["FREQ", "SUBJECT"],
    )


def test_check_dimensions_labels_keys_valid_when_empty() -> None:
    # Just test that no exception is raised.
    TsvDatasetJson(
        code="d1",
        dimensions_codes_order=["FREQ", "SUBJECT"],
        dimensions_labels={},
    )


def test_check_dimensions_labels_keys_valid_when_partial() -> None:
    # Just test that no exception is raised.
    TsvDatasetJson(
        code="d1",
        dimensions_codes_order=["FREQ", "SUBJECT"],
        dimensions_labels={"FREQ": "Frequency"},
        dimensions_values_labels={"FREQ": {"A": "Annual"}, "SUBJECT": {"S1": "Subject 1"}},
    )


def test_check_dimensions_labels_keys_invalid_when_extra() -> None:
    # TODO
    with pytest.raises(ValidationError):
        TsvDatasetJson(
            code="d1",
            dimensions_codes_order=["FREQ", "SUBJECT"],
            dimensions_labels={"COUNTRY": "France"},
        )


def test_check_dimensions_values_labels_keys_valid_when_missing() -> None:
    TsvDatasetJson(
        code="d1",
        dimensions_codes_order=["FREQ", "SUBJECT"],
        dimensions_values_labels={},
    )


def test_check_dimensions_values_labels_keys_valid_when_empty() -> None:
    TsvDatasetJson(
        code="d1",
        dimensions_codes_order=["FREQ", "SUBJECT"],
        dimensions_values_labels={},
    )


def test_check_dimensions_values_labels_keys_valid_when_partial() -> None:
    TsvDatasetJson(
        code="d1",
        dimensions_codes_order=["FREQ", "SUBJECT"],
        dimensions_values_labels={"FREQ": {"A": "Annual"}},
    )


def test_check_dimensions_values_labels_keys_invalid_when_extra() -> None:
    with pytest.raises(ValidationError):
        TsvDatasetJson(
            code="d1",
            dimensions_codes_order=["FREQ", "SUBJECT"],
            dimensions_values_labels={"COUNTRY": {"FR": "France"}},
        )


def test_create_or_replace_series_metadata() -> None:
    dataset_json = TsvDatasetJson(code="D1")
    dataset_metadata = dataset_json.to_domain_model(provider_code="P1")
    series_metadata = SeriesMetadata(id=("P1", "D1", "S1"))
    dataset_json.update_series_metadata(series_metadata, dataset_metadata=dataset_metadata)
    assert len(dataset_json.series) == 1
    assert isinstance(dataset_json.series[0], TsvSeriesJson)
    assert dataset_json.series[0].code == "S1"


def test_dataset_notes() -> None:
    dataset_json = TsvDatasetJson.parse_obj({"code": "D1", "notes": ["line 1", "line 2"]})
    assert dataset_json.notes is not None
    assert dataset_json.notes[0] == "line 1"
    assert dataset_json.notes[1] == "line 2"


def test_series_notes() -> None:
    dataset_json = TsvDatasetJson.parse_obj({"code": "D1", "series": [{"code": "D1S1", "notes": ["line 1", "line 2"]}]})
    assert dataset_json.series is not None
    assert dataset_json.series[0].notes is not None
    assert dataset_json.series[0].notes[0] == "line 1"
    assert dataset_json.series[0].notes[1] == "line 2"


def test_dates_without_time() -> None:
    now = datetime.now().date()
    dataset_metadata = DatasetMetadata(id=("P1", "D1"), next_release_at=now, updated_at=now)
    dataset_json = TsvDatasetJson.from_domain_model(dataset_metadata)
    assert dataset_json.next_release_at == now
    assert dataset_json.updated_at == now
