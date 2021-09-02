import json
from abc import abstractmethod
from typing import List

from .core import Entity, StringSequence


class Serializer:
    """Base class of all serializers."""

    @abstractmethod
    def save(self, text: StringSequence, entities: List[Entity]) -> str:
        pass


class JSONLSerializer(Serializer):
    """JSON format Serializer."""

    def save(self, text: StringSequence, entities: List[Entity]) -> str:
        """Converts a text and entities as JSONL format.

        Args:
          text: A text.
          entities: A list of entities appeared in a given text.

        Returns:
          A JSON format string.
        """
        tags = []
        for entity in entities:
            start_offset, end_offset = text.align_offsets(entity.start_offset, entity.end_offset)
            tags.append({"start_offset": start_offset, "end_offset": end_offset, "label": entity.label})
        return json.dumps(
            {
                "text": list(text),
                "tags": tags,
            }
        )


class IOB2Serializer(Serializer):
    """IOB2 format Serializer."""

    def save(self, text: StringSequence, entities: List[Entity]) -> str:
        """Converts a text and entities as IOB2 format.

        Args:
          text: A text.
          entities: A list of entities appeared in a given text.

        Returns:
          A IOB2 format string.
        """
        sequence = list(text)
        n = len(sequence)
        tags = ["O"] * n
        for entity in entities:
            start, end = text.align_offsets(entity.start_offset, entity.end_offset)

            if any(tag != "O" for tag in tags[start : end + 1]):
                raise ValueError("Overlapping spans are found.")

            tags[start] = f"B-{entity.label}"
            if start == end:
                continue
            tags[start + 1 : end + 1] = [f"I-{entity.label}"] * (end - start)

        result = []
        for item, tag in zip(sequence, tags):
            result.append(f"{item}\t{tag}")
        return "\n".join(result)


class BILOUSerializer(Serializer):
    """BILOU format Serializer."""

    def save(self, text: StringSequence, entities: List[Entity]) -> str:
        """Converts a text and entities as BILOU format.

        Args:
          text: A text.
          entities: A list of entities appeared in a given text.

        Returns:
          A BILOU format string.
        """
        sequence = list(text)
        n = len(sequence)
        tags = ["O"] * n
        for entity in entities:
            start, end = text.align_offsets(entity.start_offset, entity.end_offset)

            if any(tag != "O" for tag in tags[start : end + 1]):
                raise ValueError("Overlapping spans are found.")

            if start == end:
                tags[start] = f"U-{entity.label}"
                continue
            tags[start] = f"B-{entity.label}"
            tags[start + 1 : end] = [f"I-{entity.label}"] * (end - start - 1)
            tags[end] = f"L-{entity.label}"

        result = []
        for item, tag in zip(sequence, tags):
            result.append(f"{item}\t{tag}")
        return "\n".join(result)
