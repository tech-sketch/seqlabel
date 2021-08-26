import pytest

from seqlabel.core import Text, TokenizedText


@pytest.fixture
def text_ja() -> Text:
    return Text("日本の首都は東京都です。")


@pytest.fixture
def tokenized_text_ja() -> TokenizedText:
    return TokenizedText(["日本", "の", "首都", "は", "東京", "都", "です", "。"], [False] * 8)
