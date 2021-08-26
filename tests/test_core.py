import pytest

from phrase_matching.core import Entity, Text, TokenizedText


@pytest.mark.parametrize(
    "start_offset,end_offset,expected",
    [(3, 5, True), (0, 9, True), (0, 11, True), (0, 0, True), (-1, 5, False), (3, 12, False)],
)
def test_text_validate_offsets(text_ja: Text, start_offset: int, end_offset: int, expected: bool) -> None:
    assert text_ja.validate_offsets(start_offset, end_offset) is expected


@pytest.mark.parametrize(
    "start_offset,end_offset,expected",
    [(3, 5, (3, 5)), (0, 9, (0, 9)), (0, 11, (0, 11)), (0, 0, (0, 0))],
)
def test_text_align_offsets(text_ja: Text, start_offset: int, end_offset: int, expected: bool) -> None:
    assert text_ja.align_offsets(start_offset, end_offset) == expected


@pytest.mark.parametrize(
    "start_offset,end_offset",
    [(-1, 5), (3, 12)],
)
def test_text_align_offsets_raises_value_error(text_ja: Text, start_offset: int, end_offset: int) -> None:
    with pytest.raises(ValueError):
        text_ja.align_offsets(start_offset, end_offset)


@pytest.mark.parametrize(
    "start_offset,end_offset,expected",
    [(6, 8, True), (7, 8, False)],
)
def test_tokenized_text_validate_offsets(
    tokenized_text_ja: TokenizedText, start_offset: int, end_offset: int, expected: bool
) -> None:
    assert tokenized_text_ja.validate_offsets(start_offset, end_offset) is expected


@pytest.mark.parametrize(
    "start_offset,end_offset,expected",
    [(6, 8, (4, 5))],
)
def test_tokenized_text_align_offsets(
    tokenized_text_ja: TokenizedText, start_offset: int, end_offset: int, expected: bool
) -> None:
    assert tokenized_text_ja.align_offsets(start_offset, end_offset) == expected


@pytest.mark.parametrize(
    "start_offset,end_offset",
    [(7, 8)],
)
def test_tokenized_text_align_offsets_raiaes_value_error(
    tokenized_text_ja: TokenizedText, start_offset: int, end_offset: int
) -> None:
    with pytest.raises(ValueError):
        tokenized_text_ja.align_offsets(start_offset, end_offset)


@pytest.mark.parametrize("start_offset,end_offset,label", [(5, 3, "LOC")])
def test_entity_raises_value_error_with_invalid_offsets(start_offset: int, end_offset: int, label: str) -> None:
    with pytest.raises(ValueError):
        Entity(start_offset, end_offset, label)
