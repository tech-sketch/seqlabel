import json
from typing import List

import pytest

from seqlabel.core import Entity, StringSequence
from seqlabel.serializers import BILOUSerializer, IOB2Serializer, IOBESSerializer, JSONLSerializer


@pytest.mark.parametrize(
    "entities,expected",
    [
        (
            [Entity(6, 8, "LOC")],
            json.dumps({"text": list("日本の首都は東京都です。"), "tags": [{"start_offset": 6, "end_offset": 8, "label": "LOC"}]}),
        )
    ],
)
def test_jsonl_serializer_save(text_ja: StringSequence, entities: List[Entity], expected: str) -> None:
    serializer = JSONLSerializer()
    assert serializer.save(text_ja, entities) == expected


@pytest.mark.parametrize(
    "entities,expected",
    [
        (
            [Entity(6, 8, "LOC")],
            "日\tO\n本\tO\nの\tO\n首\tO\n都\tO\nは\tO\n東\tB-LOC\n京\tI-LOC\n都\tI-LOC\nで\tO\nす\tO\n。\tO",
        )
    ],
)
def test_iob2_serializer_save(text_ja: StringSequence, entities: List[Entity], expected: str) -> None:
    serializer = IOB2Serializer()
    assert serializer.save(text_ja, entities) == expected


@pytest.mark.parametrize(
    "entities,expected",
    [
        (
            [Entity(6, 8, "LOC")],
            "日\tO\n本\tO\nの\tO\n首\tO\n都\tO\nは\tO\n東\tB-LOC\n京\tI-LOC\n都\tE-LOC\nで\tO\nす\tO\n。\tO",
        )
    ],
)
def test_iobes_serializer_save(text_ja: StringSequence, entities: List[Entity], expected: str) -> None:
    serializer = IOBESSerializer()
    assert serializer.save(text_ja, entities) == expected


@pytest.mark.parametrize(
    "entities,expected",
    [
        (
            [Entity(6, 8, "LOC")],
            "日\tO\n本\tO\nの\tO\n首\tO\n都\tO\nは\tO\n東\tB-LOC\n京\tI-LOC\n都\tL-LOC\nで\tO\nす\tO\n。\tO",
        )
    ],
)
def test_bilou_serializer_save(text_ja: StringSequence, entities: List[Entity], expected: str) -> None:
    serializer = BILOUSerializer()
    assert serializer.save(text_ja, entities) == expected
