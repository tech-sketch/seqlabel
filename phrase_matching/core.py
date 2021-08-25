from abc import abstractmethod
from dataclasses import dataclass
from typing import Iterator, List, Tuple, Union

from tokenizations import get_alignments


class StringSequence:
    """Base class of all text."""

    @abstractmethod
    def validate_offsets(self, start_offset: int, end_offset: int) -> bool:
        pass

    @abstractmethod
    def align_offsets(self, start_offset: int, end_offset: int) -> Tuple[int, int]:
        pass

    def __repr__(self) -> str:
        return str(self)

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __getitem__(self, index: Union[int, slice]) -> Union[str, List[str]]:
        pass

    @abstractmethod
    def __iter__(self) -> Iterator[str]:
        pass


class Text(StringSequence):
    """A normal text.

    Args:
      text: A text.
    """

    def __init__(self, text: str) -> None:
        self._text = text

    def validate_offsets(self, start_offset: int, end_offset: int) -> bool:
        """Checks if character offsets are valid.

        Args:
          start_offset: A character-offset integer for a start position.
          end_offset: A character-offset integer for an end position.

        Returns:
          True if character offsets are valid, False otherwise.
        """
        return 0 <= start_offset <= end_offset < len(self._text)

    def align_offsets(self, start_offset: int, end_offset: int) -> Tuple[int, int]:
        """Converts character offsets to character offsets.

        It does nothing other than checking if character offsets are valid.
        This method is implemented for interface compatibility.

        Args:
          start_offset: A character-offset integer for a start position.
          end_offset: A character-offset integer for an end position.

        Returns:
          A tuple of character offsets.
        """
        if not self.validate_offsets(start_offset, end_offset):
            raise ValueError("Invalid character offsets.")
        return start_offset, end_offset

    def __str__(self) -> str:
        return self._text

    def __getitem__(self, index: Union[int, slice]) -> Union[str, List[str]]:
        return self._text[index]

    def __iter__(self) -> Iterator[str]:
        yield from self._text


class TokenizedText(StringSequence):
    """A tokenized text.

    Args:
      tokens: A list of tokens.
      space_after: A list of boolean indicating if a space is inserted after a token.

    """

    def __init__(self, tokens: List[str], space_after: List[bool]) -> None:
        self._tokens = tokens
        self._space_after = space_after

        mapping, _ = get_alignments(tokens, str(self))
        start_boundaries = {}
        end_boundaries = {}
        for i, indices in enumerate(mapping):
            start_boundaries[indices[0]] = i
            end_boundaries[indices[-1]] = i
        self._start_boundaries = start_boundaries
        self._end_boundaries = end_boundaries

    def validate_offsets(self, start_offset: int, end_offset: int) -> bool:
        """Checks if character offsets align with token offsets.

        Args:
          start_offset: A character-offset integer for a start position.
          end_offset: A character-offset integer for an end position.

        Returns:
          True if character offsets can be aligned, False otherwise.
        """
        return (
            start_offset <= end_offset and start_offset in self._start_boundaries and end_offset in self._end_boundaries
        )

    def align_offsets(self, start_offset: int, end_offset: int) -> Tuple[int, int]:
        """Converts character offsets to token offsets.

        Args:
          start_offset: A character-offset integer for a start position.
          end_offset: A character-offset integer for an end position.

        Returns:
          A tuple of token offsets.
        """
        if not self.validate_offsets(start_offset, end_offset):
            raise ValueError("Invalid character offsets")
        return self._start_boundaries[start_offset], self._end_boundaries[end_offset]

    def __str__(self) -> str:
        """Returns an original text before tokenization."""
        string = []
        for token, is_space in zip(self._tokens, self._space_after):
            string.append(token)
            if is_space:
                string.append(" ")
        return "".join(string)

    def __getitem__(self, index: Union[int, slice]) -> Union[str, List[str]]:
        return self._tokens[index]

    def __iter__(self) -> Iterator[str]:
        yield from self._tokens


@dataclass
class Entity:
    """An entity with a label.

    Attributes:
      start_offset: A character-offset integer with an entity starting.
      end_offset: A character-offset integer with an entity ending.
      label: A label string.
    """

    start_offset: int
    end_offset: int
    label: str

    def __post_init__(self) -> None:
        if self.end_offset < self.start_offset:
            raise ValueError("Invalid character-offset integers are given.")

    def __len__(self) -> int:
        return self.end_offset - self.start_offset + 1
