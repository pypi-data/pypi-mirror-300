import pytest

from dbnomics_data_model.model import Observation, Series, SeriesMetadata


def test_valid_series() -> None:
    series = Series(
        metadata=SeriesMetadata(id=("P1", "D1", "S1")),
        observations=[Observation(period="2014", value=0), Observation(period="2015", value=0)],
    )
    assert series.metadata.code == "S1"
    assert series.observations == [Observation(period="2014", value=0), Observation(period="2015", value=0)]


def test_unordered_observation_periods_fails() -> None:
    series = Series(
        metadata=SeriesMetadata(id=("P1", "D1", "S1")),
        observations=[Observation(period="2015", value=0), Observation(period="2014", value=0)],
    )
    # TODO
    with pytest.raises(ValidationError):
        series.validate_observation_period_order()


def test_duplicate_observation_periods_fails() -> None:
    series = Series(
        metadata=SeriesMetadata(id=("P1", "D1", "S1")),
        observations=[Observation(period="2014", value=0), Observation(period="2014", value=1)],
    )
    with pytest.raises(ValidationError):
        series.validate_observation_period_unicity()


@pytest.mark.parametrize(
    "observations",
    [
        [Observation(period="salut", value=0)],
        [Observation(period="2010-02-01-02", value=0)],
        [Observation(period="2010", value=0), Observation(period="2010-01", value=0)],
    ],
)
def test_invalid_observation_period_format_fails(observations: list[Observation]) -> None:
    series = Series(metadata=SeriesMetadata(id=("P1", "D1", "S1")), observations=observations)
    with pytest.raises(ValidationError):
        series.validate_observation_period_format()


def test_merge() -> None:
    series1 = Series(
        metadata=SeriesMetadata(id=("P1", "D1", "S1"), dimensions={"FREQ": "A"}),
        observations=[
            Observation(period="2010", value=0.1, attributes={"A1": "V1"}),
            Observation(period="2014", value=1, attributes={"A1": "V2"}),
        ],
    )
    series2 = Series(
        metadata=SeriesMetadata(id=("P1", "D1", "S1"), dimensions={"COUNTRY": "FR", "FREQ": "M"}),
        observations=[
            Observation(period="2012", value=0, attributes={"A1": "V1"}),
            Observation(period="2014", value=1.1, attributes={"A2": "V2"}),
            Observation(period="2015", value=9, attributes={"A1": "V2"}),
        ],
    )
    merged = series1.merge(series2)
    assert merged.metadata.code == "S1"
    assert merged.metadata.dimensions == {"COUNTRY": "FR", "FREQ": "M"}
    assert merged.observations == [
        Observation(period="2010", value=0.1, attributes={"A1": "V1"}),
        Observation(period="2012", value=0, attributes={"A1": "V1"}),
        Observation(period="2014", value=1.1, attributes={"A2": "V2"}),
        Observation(period="2015", value=9, attributes={"A1": "V2"}),
    ]
