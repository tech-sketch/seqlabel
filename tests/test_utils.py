from typing import List, Tuple

import pytest
from intervaltree import Interval, IntervalTree

from phrase_matching import utils


@pytest.mark.parametrize(
    "text,tokens,expected",
    [
        ("私は東京都出身です。", ["私", "は", "東京", "都", "出身", "です", "。"], [[0], [1], [2, 3], [4], [5, 6], [7, 8], [9]]),
    ],
)
def test_get_offset_mapping(text: str, tokens: List[str], expected: List[List[int]]) -> None:
    assert utils.get_offset_mapping(text, tokens) == expected


@pytest.mark.parametrize(
    "mapping,start,end,expected",
    [
        ([[0], [1], [2, 3], [4], [5, 6], [7, 8], [9]], 2, 4, (True, 2, 3)),
        ([[0], [1], [2, 3], [4], [5, 6], [7, 8], [9]], 3, 4, (False, -1, -1)),
    ],
)
def test_convert_to_token_span(mapping: List[List[int]], start: int, end: int, expected: Tuple[bool, int, int]) -> None:
    assert utils.convert_to_token_span(mapping, start, end) == expected


@pytest.mark.parametrize(
    "tree,length,expected",
    [
        (
            IntervalTree([Interval(1, 4, "LOC"), Interval(5, 6, "PER")]),
            10,
            ["O", "B-LOC", "I-LOC", "I-LOC", "O", "B-PER", "O", "O", "O", "O"],
        ),
    ],
)
def test_convert_to_tags(tree: IntervalTree, length: int, expected: List[str]) -> None:
    assert utils.convert_to_tags(tree, length) == expected
