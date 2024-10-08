import pytest

from dbnomics_data_model.model import Attribute, AttributeValue


def test_build_attribute_without_arguments_fails() -> None:
    with pytest.raises(TypeError):
        Attribute()  # type: ignore[call-arg]


def test_build_attribute_with_missing_required_kwargs_fails() -> None:
    with pytest.raises(TypeError):
        Attribute(code="A1")  # type: ignore[call-arg]


def test_build_attribute_with_required_kwargs() -> None:
    attribute = Attribute(code="A1", values=[])
    assert attribute.code == "A1"
    assert attribute.values == []


def test_build_attribute_with_label() -> None:
    attribute = Attribute(code="A1", values=[], label="A.1.")
    assert attribute.code == "A1"
    assert attribute.values == []
    assert attribute.label == "A.1."


def test_build_attribute_with_one_value() -> None:
    attribute = Attribute(code="A1", values=[AttributeValue(code="AV1")])
    assert attribute.code == "A1"
    assert attribute.values == [AttributeValue(code="AV1")]


def test_build_attribute_value_without_arguments_fails() -> None:
    with pytest.raises(TypeError):
        AttributeValue()  # type: ignore[call-arg]


def test_build_attribute_value_with_required_kwargs() -> None:
    attribute_value = AttributeValue(code="AV1")
    assert attribute_value.code == "AV1"


def test_build_attribute_value_with_label() -> None:
    attribute_value = AttributeValue(code="AV1", label="A.V.1.")
    assert attribute_value.code == "AV1"
    assert attribute_value.label == "A.V.1."


def test_merge_attributes() -> None:
    attribute = Attribute(
        code="A1",
        label="A.1.",
        values=[AttributeValue(code="AV0", label="A.V.0."), AttributeValue(code="AV1", label="A.V.1.")],
    )
    other_attribute = Attribute(
        code="A1",
        label="A-1",
        values=[AttributeValue(code="AV1", label="A-V-1"), AttributeValue(code="AV2", label="A-V-2")],
    )
    merged = attribute.merge(other_attribute)
    assert merged.code == "A1"
    assert merged.label == "A-1"
    assert merged.values == [
        AttributeValue(code="AV0", label="A.V.0."),
        AttributeValue(code="AV1", label="A-V-1"),
        AttributeValue(code="AV2", label="A-V-2"),
    ]
