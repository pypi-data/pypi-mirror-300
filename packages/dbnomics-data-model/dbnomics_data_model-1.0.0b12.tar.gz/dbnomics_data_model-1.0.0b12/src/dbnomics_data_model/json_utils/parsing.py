from pathlib import Path
from typing import Protocol, cast

import cysimdjson

from dbnomics_data_model.json_utils.types import Json

from .errors import JsonBytesParseError, JsonFileParseError, JsonStringParseError

__all__ = ["CysimdJsonParser", "JsonParser", "parse_json_bytes", "parse_json_file"]


class JsonParser(Protocol):
    def parse_bytes(self, value: bytes) -> Json: ...

    def parse_file(self, input_file: Path) -> Json: ...

    def parse_string(self, value: str) -> Json: ...


class CysimdJsonParser:
    def __init__(self) -> None:
        self._parser = cysimdjson.JSONParser()

    def parse_bytes(self, value: bytes) -> Json:
        try:
            data = self._parser.parse(value)
            return cast(Json, data.export())  # type: ignore[reportUnknownMemberType]
        except ValueError as exc:
            raise JsonBytesParseError(value=value) from exc

    def parse_file(self, input_file: Path) -> Json:
        data = self.parse_file_lazy(input_file)
        return cast(Json, data.export())  # type: ignore[reportUnknownMemberType]

    def parse_file_lazy(
        self, input_file: Path
    ) -> cysimdjson.JSONArray | cysimdjson.JSONElement | cysimdjson.JSONObject:
        try:
            return self._parser.load(str(input_file))
        except OSError as exc:
            # cysimdjson does not raise a FileNotFoundError
            if not input_file.is_file():
                raise FileNotFoundError(input_file) from exc
            raise JsonFileParseError(file_path=input_file) from exc
        except ValueError as exc:
            raise JsonFileParseError(file_path=input_file) from exc

    def parse_string(self, value: str) -> Json:
        try:
            data = self._parser.parse_string(value)
            return cast(Json, data.export())  # type: ignore[reportUnknownMemberType]
        except ValueError as exc:
            raise JsonStringParseError(value=value) from exc


default_parser = CysimdJsonParser()


def parse_json_bytes(value: bytes, *, parser: JsonParser | None = None) -> Json:
    if parser is None:
        parser = default_parser

    return parser.parse_bytes(value)


def parse_json_file(file: Path, *, parser: JsonParser | None = None) -> Json:
    if parser is None:
        parser = default_parser

    return parser.parse_file(file)
