from typing import Any, cast

from jsonalias import Json
from typedload.datadumper import Dumper
from typedload.exceptions import TypedloadException

from dbnomics_data_model.json_utils.serializing import serialize_json

from .errors import JsonDumpError

__all__ = ["create_default_dumper", "dump_as_json_bytes", "dump_as_json_data"]


def create_default_dumper() -> Dumper:
    return Dumper(hidedefault=False, isodates=True)


default_dumper = create_default_dumper()


def dump_as_json_bytes(value: Any, *, dumper: Dumper | None = None) -> bytes:
    if dumper is None:
        dumper = default_dumper

    data = dump_as_json_data(value, dumper=dumper)
    return serialize_json(data)


def dump_as_json_data(value: Any, *, dumper: Dumper | None = None) -> Json:
    if dumper is None:
        dumper = default_dumper

    try:
        data = dumper.dump(value)
    except TypedloadException as exc:
        raise JsonDumpError(value=value) from exc

    return cast(Json, data)
