from abc import abstractmethod
from typing import Dict, List

from ahocorasick import Automaton

from .core import Entity, StringSequence


class Matcher:
    @abstractmethod
    def add(self, patterns: Dict) -> None:
        pass

    @abstractmethod
    def match(self, text: StringSequence) -> List[Entity]:
        pass


class DictionaryMatcher(Matcher):
    def __init__(self) -> None:
        self._automaton = Automaton()

    def add(self, patterns: Dict) -> None:
        automaton = self._automaton
        for string, label in patterns.items():
            automaton.add_word(string, (label, len(string)))
        automaton.make_automaton()

    def match(self, text: StringSequence) -> List[Entity]:
        entities = []
        for end_offset, (label, length) in self._automaton.iter(str(text)):
            start_offset = end_offset - length + 1
            if not text.validate_offset(start_offset, end_offset):
                continue
            entities.append(Entity(start_offset, end_offset, label))
        return entities
