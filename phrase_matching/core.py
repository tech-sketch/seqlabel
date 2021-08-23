from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, List

from intervaltree import IntervalTree

from ahocorasick import Automaton
from phrase_matching import utils


def labeling_from_text(text: str, automaton: Automaton, tokenizer: Callable[[str], List[str]]) -> List[str]:
    """Attaches labels to a given text."""
    tokens = tokenizer(text)
    return labeling_from_tokens(tokens, text, automaton)


def labeling_from_tokens(tokens: List[str], text: str, automaton: Automaton) -> List[str]:
    """Attaches labels to a given text."""
    mapping = utils.get_offset_mapping(text, tokens)
    tree = IntervalTree()

    for end_char, (label, length) in automaton.iter(text):
        start_char = end_char - length + 1

        valid, start_token, end_token = utils.convert_to_token_span(mapping, start_char, end_char)

        if valid:
            end_token += 1
            spans = tree.overlap(start_token, end_token)
            if not spans:
                tree.addi(start_token, end_token, label)
            elif all(end_token - start_token > span.end - span.begin for span in spans):
                tree.remove_overlap(start_token, end_token)
                tree.addi(start_token, end_token, label)

    return utils.convert_to_tags(tree, len(tokens))


class StringSequence:
    @abstractmethod
    def validate_boundary(self, start_offset: int, end_offset: int) -> bool:
        pass

    def __repr__(self) -> str:
        return str(self)

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __getitem__(self, index: int) -> str:
        pass


class Text(StringSequence):
    def __init__(self, text: str) -> None:
        self._text = text

    def validate_boundary(self, start_offset: int, end_offset: int) -> bool:
        return 0 <= start_offset <= end_offset < len(self._text)

    def __str__(self) -> str:
        return self._text

    def __getitem__(self, index: int) -> str:
        return self._text[index]


class TokenizedText(StringSequence):
    def __init__(self, tokens: List[str], space_after: List[bool]) -> None:
        self._tokens = tokens
        self._space_after = space_after

        text = str(self)
        start_boundaries = []
        end_boundaries = []
        m = len(text)
        i = 0
        for token in tokens:
            n = len(token)
            j = 0
            while i < m and j < n and text[i] != token[j]:
                i += 1
                j += 1

            indices = []
            j = 0
            while i < m and j < n and text[i] == token[j]:
                indices.append(i)
                i += 1
                j += 1
            start_boundaries.append(indices[0])
            end_boundaries.append(indices[-1])
        self._start_boundaries = set(start_boundaries)
        self._end_boundaries = set(end_boundaries)

    def validate_boundary(self, start_offset: int, end_offset: int) -> bool:
        return (
            start_offset <= end_offset and start_offset in self._start_boundaries and end_offset in self._end_boundaries
        )

    def __str__(self) -> str:
        string = []
        for token, is_space in zip(self._tokens, self._space_after):
            string.append(token)
            if is_space:
                string.append(" ")
        return "".join(string)

    def __getitem__(self, index: int) -> str:
        return self._tokens[index]


@dataclass
class Entity:
    start_offset: int
    end_offset: int
    label: str


@dataclass
class Span:
    start_offset: int
    end_offset: int
    label: str
    sequence: List[str]
