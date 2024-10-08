from typing import cast

from dbnomics_data_model.model import DatasetMetadata, Series, SeriesMetadata
from dbnomics_data_model.storage.adapters.filesystem.model import JsonLinesSeriesItem
from dbnomics_data_model.storage.adapters.filesystem.model.json_lines_variant.json_lines_series_item import (
    ObservationJson,
    RawObservations,
    build_raw_observations_from_series,
    recombine_observations,
    separate_observations,
)


def test_build() -> None:
    series_json = JsonLinesSeriesItem(id=("P1", "D1", "S1"))
    assert not series_json.observation_attributes
    assert not series_json.observations
    assert series_json.observations_header == ["PERIOD", "VALUE"]
    series = series_json.to_domain_model()
    assert not series.observations
    dataset_metadata = DatasetMetadata(id=("P1", "D1F"))
    series_json2 = JsonLinesSeriesItem.from_series(series, dataset_metadata=dataset_metadata)
    assert not series_json2.observation_attributes
    assert not series_json2.observations
    assert series_json.observations_header == ["PERIOD", "VALUE"]


def test_build_with_two_observations() -> None:
    series_json = JsonLinesSeriesItem(
        id=("P1", "D1", "S1"),
        observations=[("PERIOD", "VALUE"), ("2000", 1000), ("2001", 1001)],
    )
    assert series_json.observation_attributes == [[], []]
    assert series_json.observations == [("2000", 1000), ("2001", 1001)]
    assert series_json.observations_header == ["PERIOD", "VALUE"]
    series = series_json.to_domain_model()
    assert not series.observations[0].attributes
    assert not series.observations[1].attributes
    dataset_metadata = DatasetMetadata(id=("P1", "D1F"))
    series_json2 = JsonLinesSeriesItem.from_series(series, dataset_metadata=dataset_metadata)
    assert series_json.observation_attributes == [[], []]
    assert series_json2.observations == [("2000", 1000), ("2001", 1001)]
    assert series_json2.observations_header == ["PERIOD", "VALUE"]


def test_build_with_two_observations_and_one_attribute() -> None:
    series_json = JsonLinesSeriesItem(
        id=("P1", "D1", "S1"),
        observations=[("PERIOD", "VALUE", "STATUS"), ("2000", 1000, "X"), ("2001", 1001, "")],
    )
    assert series_json.observation_attributes == [["X"], [""]]
    assert series_json.observations == [("2000", 1000), ("2001", 1001)]
    assert series_json.observations_header == ["PERIOD", "VALUE", "STATUS"]
    series = series_json.to_domain_model()
    assert series.observations[0].attributes["STATUS"] == "X"
    assert "STATUS" not in series.observations[1].attributes
    dataset_metadata = DatasetMetadata(id=("P1", "D1F"))
    series_json2 = JsonLinesSeriesItem.from_series(series, dataset_metadata=dataset_metadata)
    assert series_json2.observation_attributes == [["X"], [""]]
    assert series_json2.observations == [("2000", 1000), ("2001", 1001)]
    assert series_json2.observations_header == ["PERIOD", "VALUE", "STATUS"]


def test_build_with_observations_and_two_attributes() -> None:
    series_json = JsonLinesSeriesItem(
        id=("P1", "D1", "S1"),
        observations=[
            ("PERIOD", "VALUE", "STATUS", "OTHER"),
            ("2000", 1000, "X", "P"),
            ("2001", 1001, "", "Q"),
            ("2002", 1002, "", ""),
        ],
    )
    assert series_json.observation_attributes == [["X", "P"], ["", "Q"], ["", ""]]
    assert series_json.observations == [("2000", 1000), ("2001", 1001), ("2002", 1002)]
    assert series_json.observations_header == ["PERIOD", "VALUE", "STATUS", "OTHER"]
    series = series_json.to_domain_model()
    assert series.observations[0].attributes["STATUS"] == "X"
    assert series.observations[0].attributes["OTHER"] == "P"
    assert "STATUS" not in series.observations[1].attributes
    assert series.observations[1].attributes["OTHER"] == "Q"
    assert "STATUS" not in series.observations[2].attributes
    assert "OTHER" not in series.observations[2].attributes
    dataset_metadata = DatasetMetadata(id=("P1", "D1F"))
    series_json2 = JsonLinesSeriesItem.from_series(series, dataset_metadata=dataset_metadata)
    # Attributes are sorted alphabetically because SeriesMetadata does not store attribute order.
    assert series_json2.observation_attributes == [["P", "X"], ["Q", ""], ["", ""]]
    assert series_json2.observations == [("2000", 1000), ("2001", 1001), ("2002", 1002)]
    assert series_json2.observations_header == ["PERIOD", "VALUE", "OTHER", "STATUS"]


def test_build_raw_observations_from_series_no_observation() -> None:
    series = Series(metadata=SeriesMetadata(id=("P1", "D1", "S1")), observations=[])
    raw_observations = build_raw_observations_from_series(series)
    assert raw_observations == []


def test_parse_dict() -> None:
    instance = JsonLinesSeriesItem.parse_obj({"code": "S1"})
    assert instance.code == "S1"


def test_parse_dict_with_observations() -> None:
    instance = JsonLinesSeriesItem.parse_obj({"code": "S1", "observations": [["PERIOD", "VALUE"], ["2014", 1.0]]})
    assert instance.code == "S1"
    assert instance.observations_header == ["PERIOD", "VALUE"]
    assert instance.observations == [("2014", 1.0)]
    assert instance.observation_attributes == [[]]


def test_recombine_observations_no_observation() -> None:
    raw_observations = recombine_observations(
        observations=[], observations_header=["PERIOD", "VALUE"], observation_attributes=[]
    )
    assert raw_observations == []


def test_recombine_observations_one_observation() -> None:
    raw_observations = recombine_observations(
        observations=cast(list[ObservationJson], [["2014", 1.0]]),
        observations_header=["PERIOD", "VALUE"],
        observation_attributes=[[]],
    )
    assert raw_observations == [["PERIOD", "VALUE"], ["2014", 1.0]]


def test_recombine_observations_one_observation_with_an_attribute() -> None:
    raw_observations = recombine_observations(
        observations=cast(list[ObservationJson], [["2014", 1.0]]),
        observations_header=["PERIOD", "VALUE", "STATUS"],
        observation_attributes=[["X"]],
    )
    assert raw_observations == [["PERIOD", "VALUE", "STATUS"], ["2014", 1.0, "X"]]


def test_recombine_observations_two_observations_with_two_attributes() -> None:
    raw_observations = recombine_observations(
        observations=cast(list[ObservationJson], [["2014", 1.0], ["2015", 1.1]]),
        observations_header=["PERIOD", "VALUE", "STATUS", "DRAFT"],
        observation_attributes=[["A", "Y"], [None, "N"]],
    )
    assert raw_observations == [
        ["PERIOD", "VALUE", "STATUS", "DRAFT"],
        ["2014", 1.0, "A", "Y"],
        ["2015", 1.1, None, "N"],
    ]


def test_separate_observations_no_observation() -> None:
    raw_observations: RawObservations = []
    observations, observations_header, observation_attributes = separate_observations(raw_observations)
    assert observations == []
    assert observations_header == ["PERIOD", "VALUE"]
    assert observation_attributes == []


def test_separate_observations_no_observation_with_header() -> None:
    raw_observations = [["PERIOD", "VALUE"]]
    observations, observations_header, observation_attributes = separate_observations(raw_observations)
    assert observations == []
    assert observations_header == ["PERIOD", "VALUE"]
    assert observation_attributes == []


def test_separate_observations_one_observation() -> None:
    raw_observations = [["PERIOD", "VALUE"], ["2014", 1.0]]
    observations, observations_header, observation_attributes = separate_observations(raw_observations)
    assert observations == [("2014", 1.0)]
    assert observations_header == ["PERIOD", "VALUE"]
    assert observation_attributes == [[]]


def test_separate_observations_one_observation_with_an_attribute() -> None:
    raw_observations = [["PERIOD", "VALUE", "STATUS"], ["2014", 1.0, "X"]]
    observations, observations_header, observation_attributes = separate_observations(raw_observations)
    assert observations == [("2014", 1.0)]
    assert observations_header == ["PERIOD", "VALUE", "STATUS"]
    assert observation_attributes == [["X"]]


def test_separate_observations_two_observations_with_two_attributes() -> None:
    raw_observations = [["PERIOD", "VALUE", "STATUS", "DRAFT"], ["2014", 1.0, "A", "Y"], ["2015", 1.1, None, "N"]]
    observations, observations_header, observation_attributes = separate_observations(raw_observations)
    assert observations == [("2014", 1.0), ("2015", 1.1)]
    assert observations_header == ["PERIOD", "VALUE", "STATUS", "DRAFT"]
    assert observation_attributes == [["A", "Y"], [None, "N"]]
