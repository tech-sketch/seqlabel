import json
from argparse import ArgumentParser, Namespace

from conllu import parse
from seqeval.metrics import classification_report

from phrase_matching.core import labeling_from_tokens
from phrase_matching.utils import build_automaton


def main(args: Namespace) -> None:
    with open(args.dictionary) as f:
        automaton = build_automaton({key: value[0]["label"] for key, value in json.load(f).items()})

    with open(args.input) as f:
        data = parse(f.read())

    T = []
    Y = []
    for sentence in data:
        tokens = [x["form"] for x in sentence]
        tags_gold = [x["misc"]["NE"] if "NE" in x["misc"] else "O" for x in sentence]
        T.append(tags_gold)
        tags_pred = labeling_from_tokens(tokens, "".join(tokens), automaton)
        Y.append(tags_pred)

    print(classification_report(T, Y))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--dictionary", type=str, required=True)

    args = parser.parse_args()
    main(args)
