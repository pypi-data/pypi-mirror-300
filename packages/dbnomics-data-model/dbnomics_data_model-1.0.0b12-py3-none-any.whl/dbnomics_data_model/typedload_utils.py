from collections.abc import Callable
from typing import Any, TypeAlias, TypeVar

from typedload.dataloader import Loader

__all__ = ["create_default_loader", "default_loader", "TypedloadHandler"]


T = TypeVar("T")
TypedloadHandler: TypeAlias = tuple[Callable[[type[T]], bool], Callable[[Loader, Any, type[T]], T]]


def create_default_loader() -> Loader:
    return Loader(basiccast=False)


default_loader = create_default_loader()


def make_is_type(type1: type) -> Callable[[type], bool]:
    def _is_type(type2: type) -> bool:
        return type1 == type2

    return _is_type
