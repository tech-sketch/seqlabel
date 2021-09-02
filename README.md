# seqlabel: Flexible Rule-based Text Labeling

![CI badge](https://github.com/tech-sketch/seqlabel/actions/workflows/ci.yml/badge.svg)

*seqlabel* is a rule-based text labeling framework aiming at flexibility. 

## Installation

To install seqlabel:

```sh
pip install seqlabel
```

## Requirements

- Python 3.8+


## Usage

### For a normal text

First, import some classes.

```py
from seqlabel import Text
from seqlabel.matchers import DictionaryMatcher
from seqlabel.entity_filters import LongestMatchFilter, MaximizedMatchFilter
from seqlabel.serializers import IOB2Serializer
```

Initialize `Text` by giving it a text you want to label over.

```py
text = Text("Tokyo is the capital of Japan.")
```

Prepare `matcher` matching supplied patterns. You can supply patterns via Hash Map mapping string sequences to the corresponding labels. You can define your own matcher by inheriting `seqlabel.matchers.Matcher`.  

Then, apply `matcher.match` to `text`.  

```py
# Preparing Matcher
matcher = DictionaryMatcher()
# Adding patterns
matcher.add({"Tokyo": "LOC", "Japan": "LOC"})
# Matching
entities = matcher.match(text)
```

Filter unwanted entities. `LongestMatchFilter` removes overlapping entities and leaves longer entity. `MaximizedMatchFilter` removes overlapping entities and leaves as many entities as possible. You can define your own filter by inheriting `seqlabel.entity_filters.EntityFilter`.

```py
filter_a = LongestMatchFilter()
filtered_entities_a = filter_a(entities)

filter_b = MaximizedMatchFilter()
filtered_entities_b = filter_b(entities)
```

Convert entities to IOB2 format after matching and filtering. Check `seqlabel.serializers` out if you want to use other formats.

```py
serializer = IOB2Serializer()
serializer.save(text, filtered_entities_a)
```

### For a tokenized text

If you want to process a tokenized text, you need to use `TokenizedText` instead of `Text`. You could import it as follows:

```py
from seqlabel import TokenizedText
```

Initialize `TokenizedText` by giving it `tokens` and `space_after` you want to label over. `tokens` is a list of strings and `space_after` is a list of boolean indicating whether each token has a subsequent space.

```py
tokenized_text = TokenizedText(
  ["Tokyo", "is", "the", "captial", "of", "Japan", "."],
  [True, True, True, True, True, True, False]
)
```

You can use `matcher`, `filter`, and `serializer` just like a normal text, as shown above.

```py
# Mathcing
entities = matcher.match(tokenized_text)
# Filtering
filtered_entities = filter_a(entities)
# Serializing
serializer.save(tokenized_text, filtered_entities)
```
