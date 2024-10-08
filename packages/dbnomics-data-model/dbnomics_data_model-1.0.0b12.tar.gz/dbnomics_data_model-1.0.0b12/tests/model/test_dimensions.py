import pytest

from dbnomics_data_model.model import Dimension, DimensionValue


def test_build_dimension_without_arguments_fails() -> None:
    with pytest.raises(TypeError):
        Dimension()  # type: ignore[call-arg]


def test_build_dimension_with_code_only() -> None:
    dimension = Dimension(code="D1")
    assert dimension.code == "D1"
    assert dimension.values == []


def test_build_dimension_with_required_kwargs() -> None:
    dimension = Dimension(code="D1", values=[])
    assert dimension.code == "D1"
    assert dimension.values == []


def test_build_dimension_with_label() -> None:
    dimension = Dimension(code="D1", values=[], label="D.1.")
    assert dimension.code == "D1"
    assert dimension.values == []
    assert dimension.label == "D.1."


def test_build_dimension_with_one_value() -> None:
    dimension = Dimension(code="D1", values=[DimensionValue(code="DV1")])
    assert dimension.code == "D1"
    assert dimension.values == [DimensionValue(code="DV1")]


def test_build_dimension_value_without_arguments_fails() -> None:
    with pytest.raises(TypeError):
        DimensionValue()  # type: ignore[call-arg]


def test_build_dimension_value_with_required_kwargs() -> None:
    dimension_value = DimensionValue(code="DV1")
    assert dimension_value.code == "DV1"


def test_build_dimension_value_with_label() -> None:
    dimension_value = DimensionValue(code="DV1", label="D.V.1.")
    assert dimension_value.code == "DV1"
    assert dimension_value.label == "D.V.1."


def test_merge_dimensions() -> None:
    dimension = Dimension(
        code="D1",
        label="D.1.",
        values=[DimensionValue(code="DV0", label="D.V.0."), DimensionValue(code="DV1", label="D.V.1.")],
    )
    other_dimension = Dimension(
        code="D1",
        label="D-1",
        values=[DimensionValue(code="DV1", label="D-V-1"), DimensionValue(code="DV2", label="D-V-2")],
    )
    merged = dimension.merge(other_dimension)
    assert merged.code == "D1"
    assert merged.label == "D-1"
    assert merged.values == [
        DimensionValue(code="DV0", label="D.V.0."),
        DimensionValue(code="DV1", label="D-V-1"),
        DimensionValue(code="DV2", label="D-V-2"),
    ]
