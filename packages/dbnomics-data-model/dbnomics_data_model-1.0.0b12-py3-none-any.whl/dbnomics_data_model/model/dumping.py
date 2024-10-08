from typing import Any

from typedload.datadumper import Dumper

from dbnomics_data_model.json_utils import create_default_dumper
from dbnomics_data_model.model.identifiers import DatasetCode, DatasetId

__all__ = ["create_dumper"]


def create_dumper() -> Dumper:
    dumper = create_default_dumper()

    dumper.handlers.insert(0, (is_dataset_code, dump_dataset_code))
    dumper.handlers.insert(0, (is_dataset_id, dump_dataset_id))

    return dumper


def dump_dataset_code(_dumper: Dumper, value: DatasetCode, _type_: type) -> str:  # noqa: ARG001
    return str(value)


def dump_dataset_id(_dumper: Dumper, value: DatasetId, _type_: type) -> str:  # noqa: ARG001
    return str(value)


def is_dataset_code(value: Any) -> bool:
    return isinstance(value, DatasetCode)


def is_dataset_id(value: Any) -> bool:
    return isinstance(value, DatasetId)
