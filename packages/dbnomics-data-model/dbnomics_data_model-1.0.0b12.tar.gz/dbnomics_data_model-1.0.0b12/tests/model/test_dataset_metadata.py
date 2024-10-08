import pytest

from dbnomics_data_model.model import DatasetMetadata, Dimension, DimensionValue
from dbnomics_data_model.model.errors import MergeError
from dbnomics_data_model.model.validation.dataset_metadata import validate_dataset_metadata
from dbnomics_data_model.model.validation.errors import InvalidDatasetMetadata


def test_build_without_arguments_fails() -> None:
    with pytest.raises(TypeError):
        DatasetMetadata()  # type: ignore[call-arg]


def test_build_with_required_kwargs() -> None:
    dataset_metadata = DatasetMetadata(id=("P1", "D1"))
    assert dataset_metadata.code == "D1"


def test_invalid_code_fails_validation(invalid_dataset_code: str) -> None:
    dataset_metadata = DatasetMetadata(id=("P1", invalid_dataset_code))
    with pytest.raises(InvalidDatasetMetadata):
        validate_dataset_metadata(dataset_metadata)


def test_with_valid_release_code() -> None:
    dataset_metadata = DatasetMetadata(id=("P1", "foo:bar"))
    assert dataset_metadata.code == "foo:bar"


def test_invalid_release_code_fails_validation(invalid_dataset_code_release_code: str) -> None:
    dataset_metadata = DatasetMetadata(id=("P1", f"foo:{invalid_dataset_code_release_code}"))
    with pytest.raises(InvalidDatasetMetadata):
        validate_dataset_metadata(dataset_metadata)


def test_find_dimension_by_code_found() -> None:
    dataset_metadata = DatasetMetadata(
        id=("P1", "foo"),
        dimensions=[
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
                label="Frequenci",
                values=[
                    DimensionValue(code="M", label="Monthli"),
                    DimensionValue(code="Q", label="Quarterly"),
                ],
            ),
        ],
    )
    dimension = dataset_metadata.find_dimension_by_code("FREQ")
    assert dimension == dataset_metadata.dimensions[1]


def test_find_dimension_by_code_not_found() -> None:
    dataset_metadata = DatasetMetadata(
        id=("P1", "foo"),
        dimensions=[
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
                label="Frequenci",
                values=[
                    DimensionValue(code="M", label="Monthli"),
                    DimensionValue(code="Q", label="Quarterly"),
                ],
            ),
        ],
    )
    dimension = dataset_metadata.find_dimension_by_code("FOO")
    assert dimension is None


def test_merge() -> None:
    dataset_metadata = DatasetMetadata(
        id=("P1", "foo"),
        name="Foo",
        dimensions=[
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
                label="Frequenci",
                values=[
                    DimensionValue(code="M", label="Monthli"),
                    DimensionValue(code="Q", label="Quarterly"),
                ],
            ),
        ],
    )
    dataset_metadata2 = DatasetMetadata(
        id=("P1", "foo"),
        name="Foo 2",
        dimensions=[
            Dimension(
                code="FREQ",
                label="Frequency",
                values=[DimensionValue(code="A", label="Annual"), DimensionValue(code="M", label="Monthly")],
            ),
            Dimension(
                code="SUBJECT",
                label="Subject",
                values=[
                    DimensionValue(code="GDP", label="GDP"),
                ],
            ),
        ],
    )
    merged = dataset_metadata.merge(dataset_metadata2)
    assert merged.code == "foo"
    assert merged.name == "Foo 2"
    assert merged.dimensions == [
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
                DimensionValue(code="GDP", label="GDP"),
            ],
        ),
    ]


def test_merge_different_code_fails() -> None:
    dataset_metadata = DatasetMetadata(id=("P1", "foo"))
    dataset_metadata2 = DatasetMetadata(id=("P1", "bar"))
    with pytest.raises(MergeError):
        dataset_metadata.merge(dataset_metadata2)


def test_merge_different_code_succeeds_with_force_kwarg() -> None:
    dataset_metadata = DatasetMetadata(id=("P1", "foo"))
    dataset_metadata2 = DatasetMetadata(id=("P1", "bar"))
    merged = dataset_metadata.merge(dataset_metadata2, force=True)
    assert merged.code == "bar"
