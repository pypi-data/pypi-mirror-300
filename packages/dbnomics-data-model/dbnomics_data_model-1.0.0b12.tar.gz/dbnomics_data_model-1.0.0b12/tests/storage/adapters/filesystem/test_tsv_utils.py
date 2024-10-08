import pytest

from dbnomics_data_model.model import ObservationValue
from dbnomics_data_model.storage.adapters.filesystem.variants.tsv.tsv_utils import (
    InvalidTsvObservationValue,
    format_observation_value,
)


@pytest.mark.parametrize(
    ("observation_value", "expected_str"),
    [
        ("NA", "NA"),
        # zeros
        (0, "0"),
        (0.0, "0"),
        (-0, "-0"),
        (-0.0, "-0"),
        # positive
        (18, "18"),
        (18.0, "18"),
        (18.1, "18.1"),
        (30, "30"),
        (3000000000000, "3000000000000"),
        (3000000000000.0, "3000000000000"),
        (3000000000001, "3000000000001"),
        (3000000000001.0, "3000000000001"),
        # negative
        (-18, "-18"),
        (-18.0, "-18"),
        (-18.1, "-18.1"),
        (-30, "-30"),
        (-3000000000000, "-3000000000000"),
        (-3000000000000.0, "-3000000000000"),
        (-3000000000001, "-3000000000001"),
        (-3000000000001.0, "-3000000000001"),
    ],
)
def test_observation_value_to_str(observation_value: ObservationValue, expected_str: str) -> None:
    observation_value_str = format_observation_value(observation_value)
    assert observation_value_str == expected_str


def test_observation_value_to_str_error() -> None:
    with pytest.raises(InvalidTsvObservationValue):
        format_observation_value("foo")  # type: ignore[arg-type]
