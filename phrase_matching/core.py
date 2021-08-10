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
