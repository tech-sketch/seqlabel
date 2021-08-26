from typing import Dict, List

import pytest

from seqlabel.core import Entity, StringSequence
from seqlabel.matchers import DictionaryMatcher


@pytest.fixture
def dictionary_matcher() -> DictionaryMatcher:
    return DictionaryMatcher()


@pytest.fixture
def patterns() -> Dict:
    return {"東京": "LOC", "東京都": "LOC", "京都": "LOC"}


@pytest.mark.parametrize("expected", [[Entity(6, 7, "LOC"), Entity(6, 8, "LOC"), Entity(7, 8, "LOC")]])
def test_dictionary_matcher_match_text_ja(
    dictionary_matcher: DictionaryMatcher, text_ja: StringSequence, patterns: Dict, expected: List[Entity]
) -> None:
    dictionary_matcher.add(patterns)
    entities = dictionary_matcher.match(text_ja)
    assert entities == expected


@pytest.mark.parametrize("expected", [[Entity(6, 7, "LOC"), Entity(6, 8, "LOC")]])
def test_dictionary_matcher_match_tokenized_text_ja(
    dictionary_matcher: DictionaryMatcher, tokenized_text_ja: StringSequence, patterns: Dict, expected: List[Entity]
) -> None:
    dictionary_matcher.add(patterns)
    entities = dictionary_matcher.match(tokenized_text_ja)
    assert entities == expected
