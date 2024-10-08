from pathlib import Path

from dbnomics_data_model.storage.adapters.filesystem.file_system_storage import FileSystemStorage
from dbnomics_data_model.storage.errors import ProviderMetadataNotFound


def test_format_error_chain_with_simple_error() -> None:
    error = ValueError("foo")
    error_str = format_error_chain(error)
    assert error_str == "ValueError('foo')"


def test_format_error_chain_with_error_chain() -> None:
    error = ValueError("foo")
    error2 = ValueError("bar")
    error.__cause__ = error2
    error_str = format_error_chain(error)
    assert error_str == "ValueError('foo')\n  ValueError('bar')"


def test_iter_dataset_errors_fails_with_empty_dataset_dir(tmp_path: Path) -> None:
    dataset_code = "D1"
    (tmp_path / dataset_code).mkdir()
    storage = FileSystemStorage(tmp_path)
    validator = StorageValidator(storage)
    errors = list(validator.validate_datasets())
    assert len(errors) == 1


def test_iter_provider_metadata_errors_does_not_fail_without_provider_metadata(tmp_path: Path) -> None:
    storage = FileSystemStorage(tmp_path)
    validator = StorageValidator(storage)
    errors = list(validator.validate_provider_metadata())
    assert len(errors) == 1
    assert isinstance(errors[0], ProviderMetadataNotFound)
