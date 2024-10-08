from dbnomics_data_model.storage.adapters.filesystem.model import TsvSeriesJson


def test_to_series() -> None:
    series_json = TsvSeriesJson(code="S1")
    series = series_json.to_domain_model()
    assert series.metadata.code == "S1"
    assert series.observations == []
