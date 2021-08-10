from typing import Dict, List, Tuple

from intervaltree import IntervalTree

import ahocorasick


def get_offset_mapping(text: str, tokens: List[str]) -> List[List[int]]:
    """Gets mapping from token offset to char offset."""
    mapping = []
    m = len(text)
    i = 0
    for token in tokens:
        indices = []
        n = len(token)
        j = 0
        while i < m and j < n and text[i] == token[j]:
            indices.append(i)
            i += 1
            j += 1
        mapping.append(indices)
    return mapping


def convert_to_token_span(mapping: List[List[int]], start: int, end: int) -> Tuple[bool, int, int]:
    """Converts char span to token span based on mapping.

    Char and token spans are close interval: [start, end]
    """
    if start == end:
        for i, indices in enumerate(mapping):
            if indices[0] == start and len(indices) == 1:
                return True, i, i
        return False, -1, -1
    else:
        for left, indices in enumerate(mapping):
            if indices[0] == start:
                break
        for right, indices in list(enumerate(mapping))[::-1]:
            if indices[-1] == end:
                break
        if right > left:
            return True, left, right
        else:
            return False, -1, -1


def convert_to_tags(tree: IntervalTree, length: int) -> List[str]:
    """Converts spans to NER tags."""
    tags = ["O"] * length
    for span in tree:
        label = span.data
        tags[span.begin : span.end] = [f"B-{label}"] + [f"I-{label}"] * (span.end - span.begin - 1)
    return tags


def build_automaton(dictionary: Dict[str, str]) -> ahocorasick.Automaton:
    """Builds automaton from dictionary.

    Dictionary is a hash map which has phrases as keys and labels as values.
    """
    A = ahocorasick.Automaton()
    for phrase, label in dictionary.items():
        A.add_word(phrase, (label, len(phrase)))
    A.make_automaton()
    return A
