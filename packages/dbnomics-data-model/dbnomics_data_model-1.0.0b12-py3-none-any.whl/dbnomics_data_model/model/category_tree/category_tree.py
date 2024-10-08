from collections.abc import Iterator
from dataclasses import dataclass, field, replace
from typing import TYPE_CHECKING

from .category_tree_node import CategoryTreeNode, merge_category_tree_nodes, sort_category_tree_nodes

if TYPE_CHECKING:
    from .dataset_reference import DatasetReference


__all__ = ["CategoryTree"]


@dataclass(frozen=True, kw_only=True)
class CategoryTree:
    """A category tree referencing datasets."""

    children: list[CategoryTreeNode] = field(default_factory=list)

    def iter_dataset_references(self) -> Iterator["DatasetReference"]:
        """Yield datasets referenced by the category tree recursively."""
        for child in self.children:
            yield from child.iter_dataset_references()

    def merge(self, other: "CategoryTree") -> "CategoryTree":
        children = merge_category_tree_nodes(source=other.children, target=self.children)
        return replace(other, children=children)

    def sorted(self) -> "CategoryTree":
        children = sort_category_tree_nodes(self.children)
        return replace(self, children=children)
