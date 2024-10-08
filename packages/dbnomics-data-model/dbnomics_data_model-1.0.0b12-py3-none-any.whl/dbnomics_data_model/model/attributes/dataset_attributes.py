from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field, replace

from dbnomics_data_model.model.attributes.attribute import Attribute
from dbnomics_data_model.model.identifiers.attribute_code import AttributeCode
from dbnomics_data_model.model.merge_utils import merge_iterables_of_items
from dbnomics_data_model.utils import find

__all__ = ["DatasetAttributes"]


@dataclass
class DatasetAttributes:
    attributes: list[Attribute] = field(default_factory=list)

    def __iter__(self) -> Iterator[Attribute]:
        return iter(self.attributes)

    def __len__(self) -> int:
        return len(self.attributes)

    @property
    def attribute_codes(self) -> Sequence[AttributeCode]:
        return [attribute.code for attribute in self.attributes]

    def find_attribute_by_code(self, attribute_code: AttributeCode) -> Attribute | None:
        """Return the attribute having this code, or `None` if not found."""
        return find(lambda attribute: attribute.code == attribute_code, self.attributes, default=None)

    def merge(self, other: "DatasetAttributes") -> "DatasetAttributes":
        attributes = merge_iterables_of_items(
            key=lambda attribute: attribute.code,
            merge=lambda source, target: target.merge(source),
            source=other.attributes,
            target=self.attributes,
        )

        return replace(other, attributes=attributes)

    # TODO add validate method
