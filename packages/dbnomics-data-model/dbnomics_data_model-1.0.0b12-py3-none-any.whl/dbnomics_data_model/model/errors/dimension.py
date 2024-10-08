from typing import TYPE_CHECKING

from dbnomics_data_model.errors import DataModelError

if TYPE_CHECKING:
    from dbnomics_data_model.model.dimensions.dimension import Dimension
    from dbnomics_data_model.model.dimensions.dimension_value import DimensionValue


class DimensionError(DataModelError):
    def __init__(self, *, dimension: "Dimension", msg: str) -> None:
        super().__init__(msg=msg)
        self.dimension = dimension


class DatasetDimensionValueAlreadyExists(DimensionError):
    def __init__(self, *, dimension: "Dimension", dimension_value: "DimensionValue") -> None:
        msg = f"Dimension value {dimension_value.code!r} already exists in dimension {dimension.code!r}"
        super().__init__(dimension=dimension, msg=msg)
        self.dimension_value_code = dimension_value
