from dbnomics_data_model.storage.adapters.filesystem.model.category_tree_json import (
    CategoryJson,
    CategoryTreeJson,
    DatasetReferenceJson,
)


def test_to_json_data() -> None:
    category_tree_json = CategoryTreeJson(
        nodes=[
            DatasetReferenceJson(code="foo"),
            CategoryJson(code="c1", children=[DatasetReferenceJson(code="c1d1", name="bar")]),
            CategoryJson(code="c2", children=[DatasetReferenceJson(code="c2d1")]),
        ],
    )
    assert isinstance(category_tree_json.to_json_data(), list)
