from pathlib import Path

from dbnomics_data_model.storage.adapters.filesystem.storage_pool import FileSystemStoragePool


def test_iter_storages_without_children(tmp_path: Path) -> None:
    storage_pool = FileSystemStoragePool(storage_base_dir=tmp_path)
    storages = list(storage_pool.iter_storages())
    assert len(storages) == 0


def test_iter_storages_with_files(tmp_path: Path) -> None:
    for file_name in ["x.txt", "y.txt"]:
        (tmp_path / file_name).write_text("hello")
    storage_pool = FileSystemStoragePool(storage_base_dir=tmp_path)
    storages = list(storage_pool.iter_storages())
    assert len(storages) == 0


def test_iter_storages_with_children(tmp_path: Path) -> None:
    for provider_slug in ["x", "y"]:
        (tmp_path / f"{provider_slug}-json-data").mkdir()
    storage_pool = FileSystemStoragePool(storage_base_dir=tmp_path)
    storages = sorted(storage_pool.iter_storages(), key=lambda storage: storage.storage_dir.name)
    assert len(storages) == 2
    assert storages[0].storage_dir.name == "x-json-data"
    assert storages[1].storage_dir.name == "y-json-data"


def test_iter_storages_with_non_standard_repo_names(tmp_path: Path) -> None:
    for provider_slug in ["x", "y"]:
        (tmp_path / f"{provider_slug}-hello").mkdir()
    storage_pool = FileSystemStoragePool(storage_base_dir=tmp_path)
    storages = sorted(storage_pool.iter_storages(), key=lambda storage: storage.storage_dir.name)
    assert len(storages) == 2
    assert storages[0].storage_dir.name == "x-hello"
    assert storages[1].storage_dir.name == "y-hello"
