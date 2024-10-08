from operator import itemgetter, or_

from dbnomics_data_model.model.merge_utils import iter_merged_items


def test_iter_merged_items() -> None:
    current = [{"code": "z", "value": 1}, {"code": "b", "value": 2}]
    other = [{"code": "z", "value": 1.1}, {"code": "c", "value": 3.1}]
    merged = list(iter_merged_items(current, other, key=itemgetter("code"), merge=or_))
    assert merged == [{"code": "z", "value": 1.1}, {"code": "b", "value": 2}, {"code": "c", "value": 3.1}]


def test_iter_merged_items_sorted() -> None:
    current = [{"code": "z", "value": 1}, {"code": "b", "value": 2}]
    other = [{"code": "z", "value": 1.1}, {"code": "c", "value": 3.1}]
    merged = list(iter_merged_items(current, other, key=itemgetter("code"), merge=or_, sort_by_key=True))
    assert merged == [{"code": "b", "value": 2}, {"code": "c", "value": 3.1}, {"code": "z", "value": 1.1}]
