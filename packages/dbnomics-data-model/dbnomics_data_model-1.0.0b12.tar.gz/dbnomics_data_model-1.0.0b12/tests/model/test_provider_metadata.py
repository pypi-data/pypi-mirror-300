import pytest

from dbnomics_data_model.model import ProviderMetadata
from dbnomics_data_model.model.errors import MergeError


def test_build_without_arguments_fails() -> None:
    with pytest.raises(TypeError):
        ProviderMetadata()  # type: ignore[call-arg]


def test_build_with_missing_required_kwargs_fails() -> None:
    with pytest.raises(TypeError):
        ProviderMetadata(code="P1")


def test_build_with_required_kwargs() -> None:
    provider_metadata = ProviderMetadata(code="P1", website="WEBSITE")
    assert provider_metadata.code == "P1"
    assert provider_metadata.website == "WEBSITE"


def test_build_with_all_kwargs() -> None:
    provider_metadata = ProviderMetadata(
        code="P1",
        website="WEBSITE",
        attribution="ATTR",
        description="DESC",
        name="NAME",
        region="REGION",
        terms_of_use="TERMS",
    )
    assert provider_metadata.code == "P1"
    assert provider_metadata.website == "WEBSITE"
    assert provider_metadata.attribution == "ATTR"
    assert provider_metadata.description == "DESC"
    assert provider_metadata.name == "NAME"
    assert provider_metadata.region == "REGION"
    assert provider_metadata.terms_of_use == "TERMS"


def test_invalid_code_fails_validation(invalid_provider_code: str) -> None:
    provider_metadata = ProviderMetadata(code=invalid_provider_code, website="http://example.com")
    with pytest.raises(InvalidProviderMetadata):
        validate_provider_metadata(provider_metadata)


def test_invalid_terms_of_use_fails_validation() -> None:
    provider_metadata = ProviderMetadata(code="P1", terms_of_use="I am not an URL", website="http://example.com")
    with pytest.raises(InvalidProviderMetadata):
        validate_provider_metadata(provider_metadata)


def test_invalid_website_fails_validation() -> None:
    provider_metadata = ProviderMetadata(code="P1", website="I am not an URL")
    with pytest.raises(InvalidProviderMetadata):
        validate_provider_metadata(provider_metadata)


def test_merge() -> None:
    provider_metadata = ProviderMetadata(code="foo", name="Foo", website="https://foo.com")
    provider_metadata2 = ProviderMetadata(code="foo", name="Foo 2", website="https://foo2.com")
    merged = provider_metadata.merge(provider_metadata2)
    assert merged.code == "foo"
    assert merged.name == "Foo 2"
    assert merged.website == "https://foo2.com"


def test_merge_different_code_fails() -> None:
    provider_metadata = ProviderMetadata(code="foo", website="https://foo.com")
    provider_metadata2 = ProviderMetadata(code="bar", website="https://foo2.com")
    with pytest.raises(MergeError):
        provider_metadata.merge(provider_metadata2)


def test_merge_different_code_succeeds_with_force_kwarg() -> None:
    provider_metadata = ProviderMetadata(code="foo", website="https://foo.com")
    provider_metadata2 = ProviderMetadata(code="bar", website="https://foo2.com")
    merged = provider_metadata.merge(provider_metadata2, force=True)
    assert merged.code == "bar"
