from typing import TypeAlias

from jsonalias import Json as _Json

__all__ = ["Json", "JsonArray", "JsonObject"]


Json: TypeAlias = _Json
JsonArray: TypeAlias = list[_Json]
JsonObject: TypeAlias = dict[str, _Json]
