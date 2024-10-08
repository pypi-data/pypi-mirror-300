import pytest

from dbnomics_data_model.model import Dimension, DimensionValue, SeriesMetadata
from dbnomics_data_model.model.validation.errors import InvalidSeriesMetadata


def test_generate_name_empty() -> None:
    series_metadata = SeriesMetadata(id=("P1", "D1", "S1"), dimensions={"AREA": "FR", "FREQ": "A", "SUBJECT": "GDP"})
    with pytest.raises(ValueError, match="Could not generate a name from an empty list of dimensions"):
        series_metadata.generate_name(dimensions=[])


def test_generate_name_valid() -> None:
    dimensions = [
        Dimension(
            code="AREA",
            label="Geographical area",
            values=[
                DimensionValue(code="FR", label="France"),
                DimensionValue(code="DE", label="Germany"),
            ],
        ),
        Dimension(
            code="FREQ",
            label="Frequency",
            values=[
                DimensionValue(code="M", label="Monthly"),
                DimensionValue(code="Q", label="Quarterly"),
                DimensionValue(code="A", label="Annual"),
            ],
        ),
        Dimension(
            code="SUBJECT",
            label="Subject",
            values=[
                DimensionValue(code="GDP", label="Gross domestic product"),
            ],
        ),
    ]

    series_metadata = SeriesMetadata(id=("P1", "D1", "S1"), dimensions={"AREA": "FR", "FREQ": "A", "SUBJECT": "GDP"})
    series_name = series_metadata.generate_name(dimensions)
    assert series_name == "France - Annual - Gross domestic product"


def test_generate_name_missing_label() -> None:
    dimensions = [
        Dimension(
            code="AREA",
            values=[
                DimensionValue(code="FR"),
                DimensionValue(code="DE", label="Germany"),
            ],
        ),
        Dimension(
            code="FREQ",
            label="Frequency",
            values=[
                DimensionValue(code="M", label="Monthly"),
                DimensionValue(code="Q", label="Quarterly"),
                DimensionValue(code="A", label="Annual"),
            ],
        ),
        Dimension(
            code="SUBJECT",
            label="Subject",
            values=[
                DimensionValue(code="GDP", label="Gross domestic product"),
            ],
        ),
    ]

    series_metadata = SeriesMetadata(id=("P1", "D1", "S1"), dimensions={"AREA": "FR", "FREQ": "A", "SUBJECT": "GDP"})
    series_name = series_metadata.generate_name(dimensions)
    assert series_name == "FR - Annual - Gross domestic product"


def test_generate_name_invalid() -> None:
    dimensions = [
        Dimension(
            code="AREA",
            label="Geographical area",
            values=[
                DimensionValue(code="FR", label="France"),
                DimensionValue(code="DE", label="Germany"),
            ],
        ),
        Dimension(
            code="FREQ",
            label="Frequency",
            values=[
                DimensionValue(code="M", label="Monthly"),
                DimensionValue(code="Q", label="Quarterly"),
                DimensionValue(code="A", label="Annual"),
            ],
        ),
        Dimension(
            code="SUBJECT",
            label="Subject",
            values=[
                DimensionValue(code="GDP", label="Gross domestic product"),
            ],
        ),
    ]

    series_metadata = SeriesMetadata(id=("P1", "D1", "S1"), dimensions={"FREQ": "A", "SUBJECT": "GDP"})
    with pytest.raises(InvalidSeriesMetadata):
        series_metadata.generate_name(dimensions)


def test_generate_name_precision() -> None:
    dimensions = [
        Dimension(
            code="AREA",
            label="Geographical area",
            values=[
                DimensionValue(code="FR", label="France"),
                DimensionValue(code="DE", label="Germany"),
            ],
        ),
        Dimension(
            code="FREQ",
            label="Frequency",
            values=[
                DimensionValue(code="M", label="Monthly"),
                DimensionValue(code="Q", label="Quarterly"),
                DimensionValue(code="A", label="Annual"),
            ],
        ),
        Dimension(
            code="SUBJECT",
            label="Subject",
            values=[
                DimensionValue(code="GDP1", label="Gross domestic product"),
                DimensionValue(code="GDP2", label="Gross domestic product"),
            ],
        ),
    ]

    series_metadata = SeriesMetadata(id=("P1", "D1", "S1"), dimensions={"AREA": "FR", "FREQ": "A", "SUBJECT": "GDP1"})
    series_name = series_metadata.generate_name(dimensions)
    assert series_name == "France - Annual - Gross domestic product (GDP1)"
