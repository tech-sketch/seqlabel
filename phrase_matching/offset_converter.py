from typing import List

from .core import Entity, Span, StringSequence


class OffsetConverter:
    def convert(self, text: StringSequence, entities: List[Entity]) -> List[Span]:
        entities = sorted(entities, key=lambda entity: entity.start_offset)
        spans = []
        for entity in entities:
            start_offset, end_offset = text.align_offset(entity.start_offset, entity.end_offset)
            spans.append(Span(start_offset, end_offset, entity.label, text[start_offset : end_offset + 1]))
        return spans
