from pathlib import Path
from typing import Any, TypeVar, cast

from jsonalias import Json
from typedload.dataloader import Loader
from typedload.exceptions import TypedloadException

from dbnomics_data_model.json_utils.parsing import JsonParser, parse_json_file
from dbnomics_data_model.typedload_utils import create_default_loader, default_loader

from .errors import JsonParseTypeError

__all__ = ["load_json_data", "load_json_file"]


T = TypeVar("T")


def create_json_loader() -> Loader:
    loader = create_default_loader()
    loader.frefs = cast(dict[str, type], {"Json": Json})
    return loader


json_loader = create_json_loader()


def load_json_data(data: Any, *, loader: Loader | None = None, type_: type[T]) -> T:
    if loader is None:
        loader = default_loader

    try:
        return loader.load(data, type_=type_)
    except TypedloadException as exc:
        raise JsonParseTypeError(data=data, expected_type=type_) from exc


def load_json_file(file: Path, *, loader: Loader | None = None, parser: JsonParser | None = None, type_: type[T]) -> T:
    if loader is None:
        loader = json_loader

    data = parse_json_file(file, parser=parser)
    return load_json_data(data, loader=loader, type_=type_)
