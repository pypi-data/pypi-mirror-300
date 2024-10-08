from typing import cast

from typedload.dataloader import Loader

from dbnomics_data_model.typedload_utils import create_default_loader

__all__ = ["filesystem_model_loader"]


def create_filesystem_model_loader() -> Loader:
    from .category_tree_json import CategoryTreeNodeJson

    loader = create_default_loader()
    loader.frefs = cast(dict[str, type], {"CategoryTreeNodeJson": CategoryTreeNodeJson})
    return loader


filesystem_model_loader = create_filesystem_model_loader()
