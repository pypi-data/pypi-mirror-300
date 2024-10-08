from dataclasses import dataclass
from typing import Self, cast

from jsonalias import Json

from dbnomics_data_model.json_utils.dumping import dump_as_json_data
from dbnomics_data_model.json_utils.errors import JsonDumpError, JsonParseTypeError
from dbnomics_data_model.json_utils.loading import load_json_data
from dbnomics_data_model.json_utils.types import JsonObject
from dbnomics_data_model.storage.adapters.filesystem.errors.json_model import JsonModelDumpError, JsonModelParseError


@dataclass
class BaseJsonObjectModel:
    @classmethod
    def from_json_data(cls, data: Json) -> Self:
        from .loading import filesystem_model_loader

        try:
            return load_json_data(data, loader=filesystem_model_loader, type_=cls)
        except JsonParseTypeError as exc:
            raise JsonModelParseError(data=data) from exc

    def to_json_data(self) -> JsonObject:
        try:
            data = dump_as_json_data(self)
        except JsonDumpError as exc:
            raise JsonModelDumpError(obj=self) from exc
        return cast(JsonObject, data)
