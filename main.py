import json
from argparse import ArgumentParser, Namespace

from conllu import parse

from phrase_matching.core import TokenizedText
from phrase_matching.entity_filters import LongestMatchFilter
from phrase_matching.matchers import DictionaryMatcher
from phrase_matching.serializers import IOB2Serializer


def main(args: Namespace) -> None:
    with open(args.dictionary) as f:
        dictionary = json.load(f)

    with open(args.input) as f:
        data = parse(f.read())

    matcher = DictionaryMatcher()
    matcher.add({key: value[0]["label"] for key, value in dictionary.items()})

    filter_ = LongestMatchFilter()
    serializer = IOB2Serializer()

    for sentence in data:
        tokens = [x["form"] for x in sentence]
        space_after = [x["misc"]["SpaceAfter"] == "Yes" for x in sentence]

        text = TokenizedText(tokens, space_after)

        entities = matcher.match(text)
        filtered = filter_(entities)
        print(serializer.save(text, filtered))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--dictionary", type=str, required=True)

    args = parser.parse_args()
    main(args)
