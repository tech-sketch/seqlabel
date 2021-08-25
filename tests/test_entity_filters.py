from typing import List

import pytest

from phrase_matching.core import Entity
from phrase_matching.entity_filters import LongestMatchFilter, overlap


@pytest.fixture
def longest_match_filter() -> LongestMatchFilter:
    return LongestMatchFilter()


@pytest.mark.parametrize(
    "entity_a,entity_b,expected",
    [
        (Entity(0, 3, "LOC"), Entity(2, 4, "LOC"), True),
        (Entity(0, 3, "LOC"), Entity(3, 5, "LOC"), True),
        (Entity(0, 3, "LOC"), Entity(0, 3, "LOC"), True),
        (Entity(0, 3, "LOC"), Entity(5, 7, "LOC"), False),
        (Entity(0, 3, "LOC"), Entity(4, 7, "LOC"), False),
    ],
)
def test_overlap(entity_a: Entity, entity_b: Entity, expected: bool) -> None:
    assert overlap(entity_a, entity_b) is expected
    assert overlap(entity_b, entity_a) is expected


@pytest.mark.parametrize(
    "entities,expected",
    [
        ([Entity(0, 5, "LOC"), Entity(4, 7, "LOC"), Entity(6, 8, "LOC")], [Entity(0, 5, "LOC"), Entity(6, 8, "LOC")]),
        ([Entity(0, 3, "LOC"), Entity(2, 7, "LOC"), Entity(6, 8, "LOC")], [Entity(2, 7, "LOC")]),
    ],
)
def test_longest_match_filter(
    longest_match_filter: LongestMatchFilter, entities: List[Entity], expected: List[Entity]
) -> None:
    assert longest_match_filter(entities) == expected
