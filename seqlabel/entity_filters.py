from abc import abstractmethod
from typing import List

from .core import Entity


def overlap(a: Entity, b: Entity) -> bool:
    """Checks if one entity overlaps with another entity.

    Args:
      a: One entity.
      b: Another entity.

    Returns:
      True if there is an overlap, False otherwise.
    """
    return a.start_offset <= b.end_offset and b.start_offset <= a.end_offset


class EntityFilter:
    """Base class of all entity filters."""

    @abstractmethod
    def __call__(self, entities: List[Entity]) -> List[Entity]:
        pass


class LongestMatchFilter:
    """Entity filter prioritizes entity length."""

    def __call__(self, entities: List[Entity]) -> List[Entity]:
        """Removes overlapping entities and leaves the longest entity.

        Args:
          entities: A list of entities.

        Returns:
          A list of entities without any overlaps.
        """
        entities = sorted(entities, key=len, reverse=True)
        filtered: List[Entity] = []
        for cur in entities:
            if all(not overlap(cur, prev) for prev in filtered):
                filtered.append(cur)
        filtered.sort(key=lambda entity: entity.start_offset)
        return filtered


class MaximizedMatchFilter:
    """Entity filter prioritizes the number of entities."""

    def __call__(self, entities: List[Entity]) -> List[Entity]:
        """Removes overlapping entities and leaves as many entities as possible.

        Args:
          entities: A list of entities.

        Returns:
          A list of entities without any overlaps.
        """
        entities = sorted(entities, key=lambda entity: entity.end_offset)
        filtered: List[Entity] = []
        for entity in entities:
            if not filtered:
                filtered.append(entity)
            elif not overlap(filtered[-1], entity):
                filtered.append(entity)
        return filtered
