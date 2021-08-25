from abc import abstractmethod
from typing import List

from .core import Entity


def overlap(a: Entity, b: Entity) -> bool:
    return a.start_offset <= b.end_offset and a.start_offset <= b.end_offset


class EntityFilter:
    @abstractmethod
    def __call__(self, entities: List[Entity]) -> List[Entity]:
        pass


class LongestMatchFilter:
    def __call__(self, entities: List[Entity]) -> List[Entity]:
        # TODO: not efficient
        entities = sorted(entities, key=len, reverse=True)
        filtered: List[Entity] = []
        for cur in entities:
            if all(not overlap(cur, prev) for prev in filtered):
                filtered.append(cur)
        return filtered
