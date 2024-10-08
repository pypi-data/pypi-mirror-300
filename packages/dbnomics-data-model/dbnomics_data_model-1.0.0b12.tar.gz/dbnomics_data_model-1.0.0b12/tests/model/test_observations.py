import pytest

from dbnomics_data_model.model import Observation
from dbnomics_data_model.model.validation.errors import ValidationError


def test_init_observation_without_args_fails() -> None:
    with pytest.raises(TypeError):
        Observation()  # type: ignore[call-arg]


def test_init_observation_with_period_only_fails() -> None:
    with pytest.raises(TypeError):
        Observation(period="2000")  # type: ignore[call-arg]


def test_init_observation_with_value_only_fails() -> None:
    with pytest.raises(TypeError):
        Observation(value=0)  # type: ignore[call-arg]


def test_init_observation_with_period_and_value() -> None:
    observation = Observation(period="2000", value=0)
    assert observation.period == "2000"
    assert observation.value == 0
    assert observation.attributes == {}


def test_init_observation_with_one_attribute() -> None:
    observation = Observation(period="2000", value=0, attributes={"A1": "V1"})
    assert observation.period == "2000"
    assert observation.value == 0
    assert observation.attributes == {"A1": "V1"}


@pytest.mark.parametrize(
    "observation",
    [Observation(period="salut", value=0), Observation(period="2010-02-01-02", value=0)],
)
def test_init_observation_with_invalid_period_fails(observation: Observation) -> None:
    # TODO
    with pytest.raises(ValidationError):
        observation.validate()
