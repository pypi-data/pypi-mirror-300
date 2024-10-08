from datetime import datetime

import pytest

from dbnomics_data_model.model import DatasetMetadata, Series, SeriesMetadata
from dbnomics_data_model.storage.adapters.filesystem.model import BaseSeriesJson


class DummySeriesJson(BaseSeriesJson):
    """Dummy model allowing to test BaseSeriesJson.

    BaseSeriesJson can't be instanciated because it has an abstract method.
    """

    def _to_series_domain_model(self, series_metadata: SeriesMetadata) -> Series:  # pragma: no cover
        raise NotImplementedError


def test_from_series_metadata() -> None:
    dataset_metadata = DatasetMetadata(id=("P1", "D1"))
    series_metadata = SeriesMetadata(id=("P1", "D1", "S1"), notes="This is a note")
    series_json = DummySeriesJson.from_domain_model(series_metadata, dataset_metadata=dataset_metadata)
    assert series_json.notes is not None
    assert series_json.notes[0] == "This is a note"


def test_dates_without_time() -> None:
    dataset_metadata = DatasetMetadata(id=("P1", "D1"))
    now = datetime.now().date()
    series_metadata = SeriesMetadata(id=("P1", "D1", "S1"), next_release_at=now, updated_at=now)
    series_json = DummySeriesJson.from_domain_model(series_metadata, dataset_metadata=dataset_metadata)
    assert series_json.next_release_at == now
    assert series_json.updated_at == now


def test_dimensions_as_dict() -> None:
    series_json = DummySeriesJson(id=("P1", "D1", "S1"), dimensions={"FREQ": "Q"})
    series_metadata = series_json._to_metadata_domain_model()  # noqa: SLF001
    assert series_metadata.dimensions == {"FREQ": "Q"}


def test_dimensions_as_dict_ignores_dimensions_codes_order() -> None:
    series_json = DummySeriesJson(id=("P1", "D1", "S1"), dimensions={"FREQ": "Q"})
    series_metadata = series_json._to_metadata_domain_model(dimensions_codes_order=["foo"])  # noqa: SLF001
    assert series_metadata.dimensions == {"FREQ": "Q"}


def test_dimensions_as_list() -> None:
    series_json = DummySeriesJson(id=("P1", "D1", "S1"), dimensions=["Q"])
    series_metadata = series_json._to_metadata_domain_model(dimensions_codes_order=["FREQ"])  # noqa: SLF001
    assert series_metadata.dimensions == {"FREQ": "Q"}


def test_dimensions_as_list_with_invalid_dimensions_codes_order_fails() -> None:
    series_json = DummySeriesJson(id=("P1", "D1", "S1"), dimensions=["Q"])
    with pytest.raises(ValueError, match="dimensions_codes_order and series dimensions must have the same length"):
        series_json._to_metadata_domain_model(dimensions_codes_order=["FREQ", "FOO"])  # noqa: SLF001


def test_dimensions_as_list_without_dimensions_codes_order_fails() -> None:
    series_json = DummySeriesJson(id=("P1", "D1", "S1"), dimensions=["Q"])
    with pytest.raises(ValueError, match="dimensions_codes_order must be given when dimensions is a list"):
        series_json._to_metadata_domain_model()  # noqa: SLF001


def test_invalid_type_for_dimensions() -> None:
    # TODO
    with pytest.raises(ValidationError):
        DummySeriesJson(id=("P1", "D1", "S1"), dimensions="salut")
