# seqlabel: Easy Distant Supervision Dataset Construction


## Usage

```py
from seqlabel import Text
from seqlabel.matchers import DictionaryMatcher
from seqlabel.serializers import IOB2Serializer


text = Text("Tokyo is the capital of Japan.")

# Preparing Matcher
matcher = DictionaryMatcher()

# Adding patterns
matcher.add({"Tokyo": "LOC", "Japan": "LOC"})

# Matching
entities = matcher.match(text)

serializer = IOB2Serializer()
# Converting a IOB2 format text
serializer.save(text, entities)
```
