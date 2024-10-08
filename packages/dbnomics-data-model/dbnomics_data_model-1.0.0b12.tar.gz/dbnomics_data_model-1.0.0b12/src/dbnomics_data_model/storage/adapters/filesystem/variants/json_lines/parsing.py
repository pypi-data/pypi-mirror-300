from typing import Any, cast

import cysimdjson
from jsonalias import Json

from dbnomics_data_model.json_utils.errors import JsonBytesParseError, JsonParseTypeError


def parse_json_line_code(line: bytes) -> str:
    # Parse lazily because we just want to read the "code" property.

    parser = cysimdjson.JSONParser()
    data = parser.parse(line)
    if not isinstance(data, dict):
        raise JsonParseTypeError(data=cast(Json, data), expected_type=dict)

    try:
        code: Any = data["code"]
    except KeyError as exc:
        raise JsonBytesParseError(value=line) from exc

    if not isinstance(code, str):
        raise JsonBytesParseError(value=line)

    return code
