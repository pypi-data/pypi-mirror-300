from dataclasses import dataclass
from typing import TypeAlias, cast

from jsonalias import Json

from dbnomics_data_model.json_utils import JsonObject
from dbnomics_data_model.validation.errors.validation_error_code import ValidationErrorCode
from dbnomics_data_model.validation.errors.validation_error_code_registry import ValidationErrorCodeRegistry

ValidationErrorPath: TypeAlias = list[tuple[str, str]]


@dataclass(kw_only=True)
class ValidationErrorData:
    code: ValidationErrorCode
    extra: JsonObject | None = None
    path: ValidationErrorPath | None

    def to_json(self) -> JsonObject:
        validation_error_code_info = ValidationErrorCodeRegistry.get(self.code)

        result: JsonObject = {
            "code": self.code,
            "description": validation_error_code_info.description,
            "level": validation_error_code_info.level.value,
        }

        if self.extra:
            result["extra"] = self.extra

        if self.path is not None:
            result["path"] = cast(Json, self.path)

        return result
