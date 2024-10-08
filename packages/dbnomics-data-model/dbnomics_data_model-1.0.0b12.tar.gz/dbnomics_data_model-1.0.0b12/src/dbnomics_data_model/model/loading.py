from typing import Any, Protocol, Self, TypeVar

from typedload.dataloader import Loader
from typedload.exceptions import TypedloadException, TypedloadTypeError

from dbnomics_data_model.model import DatasetCode, DatasetId, SeriesCode
from dbnomics_data_model.model.identifiers.errors import DatasetCodeParseError
from dbnomics_data_model.model.identifiers.series_id import SeriesId
from dbnomics_data_model.model.identifiers.simple_code import SimpleCode
from dbnomics_data_model.typedload_utils import create_default_loader, make_is_type

__all__ = ["create_loader"]


def create_loader() -> Loader:
    loader = create_default_loader()

    loader.strconstructed = {SeriesCode, SimpleCode}

    for type_ in (DatasetCode, DatasetId, SeriesId):
        loader.handlers.insert(0, (make_is_type(type_), load_parsable))

    return loader


class SupportsParse(Protocol):
    @classmethod
    def parse(cls, value: str) -> Self: ...


TSupportsParse = TypeVar("TSupportsParse", bound=SupportsParse)


def load_parsable(_loader: Loader, value: Any, type_: type[TSupportsParse]) -> TSupportsParse:
    if not isinstance(value, str):
        msg = f"Expected a str to be parsed as a {type_.__name__}"
        raise TypedloadTypeError(msg, type_=type_, value=value)

    try:
        return type_.parse(value)
    except DatasetCodeParseError as exc:
        raise TypedloadException(str(exc), type_=type_, value=value) from exc
