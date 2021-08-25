import json
from abc import abstractmethod
from typing import List

from .core import Span, StringSequence


class Serializer:
    @abstractmethod
    def save(self, text: StringSequence, spans: List[Span]) -> str:
        pass


class JSONLSerializer(Serializer):
    def save(self, text: StringSequence, spans: List[Span]) -> str:
        data = {
            "text": list(text),
            "tags": [(span.start_offset, span.end_offset, span.label) for span in spans],
        }
        return json.dumps(data)


class IOB2Serializer(Serializer):
    def save(self, text: StringSequence, spans: List[Span]) -> str:
        sequence = list(text)
        n = len(sequence)
        tags = ["O"] * n
        for span in spans:
            start, end = span.start_offset, span.end_offset

            if any(tag != "O" for tag in tags[start : end + 1]):
                raise ValueError("Overlapping spans are found.")

            tags[start] = f"B-{span.label}"
            if start == end:
                continue
            tags[start + 1 : end + 1] = [f"I-{span.label}"] * (end - start)

        result = []
        for item, tag in zip(sequence, tags):
            result.append(f"{item}\t{tag}")
        return "\n".join(result)


class BILOUSerializer(Serializer):
    def save(self, text: StringSequence, spans: List[Span]) -> str:
        sequence = list(text)
        n = len(sequence)
        tags = ["O"] * n
        for span in spans:
            start, end = span.start_offset, span.end_offset

            if any(tag != "O" for tag in tags[start : end + 1]):
                raise ValueError("Overlapping spans are found.")

            if start == end:
                tags[start] = f"U-{span.label}"
                continue
            tags[start] = f"B-{span.label}"
            tags[start + 1 : end] = [f"I-{span.label}"] * (end - start - 1)
            tags[end] = f"L-{span.label}"

        result = []
        for item, tag in zip(sequence, tags):
            result.append(f"{item}\t{tag}")
        return "\n".join(result)
