from dbnomics_data_model.model import Category, CategoryTree, DatasetReference


def test_iter_dataset_references() -> None:
    category_tree = CategoryTree(
        children=[
            DatasetReference(code="bar"),
            Category(code="c1", children=[DatasetReference(code="c1d1", name="hello")]),
            Category(code="c2", children=[DatasetReference(code="c2d1")]),
        ],
    )
    dataset_references = list(category_tree.iter_dataset_references())
    assert dataset_references == [
        DatasetReference(code="bar"),
        DatasetReference(code="c1d1", name="hello"),
        DatasetReference(code="c2d1"),
    ]


def test_iter_dataset_references_no_children() -> None:
    category_tree = CategoryTree(
        children=[
            DatasetReference(code="bar"),
            Category(code="c1", children=[]),
            Category(code="c2", children=[DatasetReference(code="c2d1")]),
        ],
    )
    dataset_references = list(category_tree.iter_dataset_references())
    assert dataset_references == [
        DatasetReference(code="bar"),
        DatasetReference(code="c2d1"),
    ]


def test_merge() -> None:
    category_tree = CategoryTree(
        children=[
            DatasetReference(code="foo"),
            Category(code="c1", children=[DatasetReference(code="c1d1")]),
        ],
    )
    category_tree2 = CategoryTree(
        children=[
            DatasetReference(code="bar"),
            Category(
                code="c1",
                children=[
                    DatasetReference(code="c1d0"),
                    DatasetReference(code="c1d1", name="hello"),
                    DatasetReference(code="c1d2"),
                ],
            ),
            Category(code="c2", children=[DatasetReference(code="c2d1")]),
        ],
    )
    merged = category_tree.merge(category_tree2)
    assert merged.children[0].code == "foo"
    assert merged.children[1].code == "c1"
    assert isinstance(merged.children[1], Category)
    assert merged.children[1].children[0].code == "c1d1"
    assert merged.children[1].children[0].name == "hello"
    assert merged.children[1].children[1].code == "c1d0"
    assert merged.children[1].children[2].code == "c1d2"
    assert merged.children[2].code == "bar"
    assert merged.children[3].code == "c2"
