import pytest

from dbnomics_data_model.model import ProviderMetadata
from dbnomics_data_model.storage.adapters.filesystem.model import ProviderJson


def test_build_without_arguments_fails() -> None:
    with pytest.raises(PydanyticValidationError):
        ProviderJson()  # type: ignore[call-arg]


def test_build_with_missing_required_kwargs_fails() -> None:
    with pytest.raises(PydanyticValidationError):
        ProviderJson(code="P1")  # type: ignore[call-arg]


def test_build_with_required_kwargs() -> None:
    provider_json = ProviderJson(code="P1", website="WEBSITE")
    assert provider_json.code == "P1"
    assert provider_json.website == "WEBSITE"


def test_build_with_all_kwargs() -> None:
    provider_json = ProviderJson(
        code="P1",
        website="WEBSITE",
        attribution="ATTR",
        description="DESC",
        name="NAME",
        region="REGION",
        terms_of_use="TERMS",
    )
    assert provider_json.code == "P1"
    assert provider_json.website == "WEBSITE"
    assert provider_json.attribution == "ATTR"
    assert provider_json.description == "DESC"
    assert provider_json.name == "NAME"
    assert provider_json.region == "REGION"
    assert provider_json.terms_of_use == "TERMS"


def test_invalid_code_does_not_fail(invalid_provider_code: str) -> None:
    provider_json = ProviderJson(code=invalid_provider_code, website="http://example.com")
    assert provider_json.code == invalid_provider_code


def test_invalid_terms_of_use_does_not_fail() -> None:
    invalid_terms_of_use = "I am not an URL"
    provider_json = ProviderJson(code="P1", terms_of_use=invalid_terms_of_use, website="http://example.com")
    assert provider_json.terms_of_use == invalid_terms_of_use


def test_invalid_website_does_not_fail() -> None:
    invalid_website = "I am not an URL"
    provider_json = ProviderJson(code="P1", website=invalid_website)
    assert provider_json.website == invalid_website


def test_build_from_provider_metadata() -> None:
    provider_metadata = ProviderMetadata(
        code="P1",
        website="WEBSITE",
        attribution="ATTR",
        description="DESC",
        name="NAME",
        region="REGION",
        terms_of_use="TERMS",
    )
    provider_json = ProviderJson.from_domain_model(provider_metadata)
    assert provider_json.code == "P1"
    assert provider_json.website == "WEBSITE"
    assert provider_json.attribution == "ATTR"
    assert provider_json.description == "DESC"
    assert provider_json.name == "NAME"
    assert provider_json.region == "REGION"
    assert provider_json.terms_of_use == "TERMS"


def test_convert_to_provider_metadata() -> None:
    provider_json = ProviderJson(
        code="P1",
        website="http://example.com",
        attribution="ATTR",
        description="DESC",
        name="NAME",
        region="REGION",
        terms_of_use="http://example.com/terms",
    )
    provider_metadata = provider_json.to_domain_model()
    assert provider_metadata.code == "P1"
    assert provider_metadata.website == "http://example.com"
    assert provider_metadata.attribution == "ATTR"
    assert provider_metadata.description == "DESC"
    assert provider_metadata.name == "NAME"
    assert provider_metadata.region == "REGION"
    assert provider_metadata.terms_of_use == "http://example.com/terms"
