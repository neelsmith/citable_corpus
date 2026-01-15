# citable_corpus

A Python library for working with a corpus of texts canonically citable by CTS URN references.

## Overview

`citable_corpus` lets you work with texts citable by CTS URNs(Canonical Text Services URN).

## Features

- **Multiple input formats**: Create corpora from delimited strings, or from files or URLs with data in CEX format.
- **Retrieval based on URN logic**: Querying passages by URN recognizes work and passage hierarchies, as well as passage ranges.
- **CEX support**: Native support for the [CEX](https://cite-architecture.github.io/citedx/CEX-spec-3.0.1/) (CITE Exchange) format
- **Type-safe**: Built with Pydantic for robust data validation

## Installation

```bash
pip install citable_corpus
```

## Quick Start

### Creating a Corpus

#### From a delimited string

```python
from citable_corpus import CitableCorpus

text = """urn:cts:latinLit:phi0959.phi006:1.1|Lorem ipsum
urn:cts:latinLit:phi0959.phi006:1.2|Dolor sit amet."""

corpus = CitableCorpus.from_string(text)
print(f"Loaded {len(corpus.passages)} passages")
```

#### From a CEX file

```python
corpus = CitableCorpus.from_cex_file("path/to/file.cex")
```

#### From a URL

```python
url = "https://example.com/corpus.cex"
corpus = CitableCorpus.from_cex_url(url)
```

### Working with Passages

Each passage in a corpus is a `CitablePassage` object with a URN and text:

```python
passage = corpus.passages[0]
print(passage.urn)   # The CtsUrn object
print(passage.text)  # The text content
print(str(passage))  # "urn:...: text"
```

### Retrieving Passages

#### Retrieve a single passage by exact URN

```python
from urn_citation import CtsUrn

ref = CtsUrn.from_string("urn:cts:latinLit:stoa1263.stoa001.hc:pr.1")
results = corpus.retrieve(ref)
```

#### Retrieve all passages from a work section

```python
# Get all passages from the preface (pr.) section
ref = CtsUrn.from_string("urn:cts:latinLit:stoa1263.stoa001.hc:pr")
results = corpus.retrieve(ref)
```

#### Retrieve all passages from a work

```python
# Get all passages from the work (note the trailing colon)
ref = CtsUrn.from_string("urn:cts:latinLit:stoa1263.stoa001.hc:")
results = corpus.retrieve(ref)
```

#### Retrieve a range of passages

```python
# Get passages from pr.1 through pr.5
ref = CtsUrn.from_string("urn:cts:latinLit:stoa1263.stoa001.hc:pr.1-pr.5")
results = corpus.retrieve_range(ref)

# Or use retrieve(), which automatically detects ranges
results = corpus.retrieve(ref)
```

## API Reference

### CitableCorpus

The main class for working with a corpus of citable texts.

**Class Methods:**
- `from_string(s: str, delimiter: str = "|")` - Create from delimited text
- `from_cex_file(f: str, delimiter: str = "|")` - Create from a CEX file
- `from_cex_url(url: str, delimiter: str = "|")` - Create from a URL

**Instance Methods:**
- `retrieve(ref: CtsUrn)` - Retrieve passages matching a URN reference
- `retrieve_range(ref: CtsUrn)` - Retrieve passages in a URN range
- `len()` - Get the number of passages in the corpus

**Attributes:**
- `passages: List[CitablePassage]` - The list of passages in the corpus

### CitablePassage

Represents a single citable passage of text.

**Class Methods:**
- `from_string(src: str, delimiter: str = "|")` - Create from a delimited string

**Attributes:**
- `urn: CtsUrn` - The CTS URN identifying this passage
- `text: str` - The text content of the passage

## Examples

### Filtering and Processing

```python
# Find all passages containing a specific word
matches = [p for p in corpus.passages if "Zeus" in p.text]

# Get URNs of all passages
urns = [p.urn for p in corpus.passages]

# Count passages by work
from collections import Counter
works = Counter(p.urn.work for p in corpus.passages)
```

### Working with CEX Data

The library supports the CEX (CITE Exchange) format, commonly used in digital classics:

```python
# Load a CEX file with Hyginus fables
corpus = CitableCorpus.from_cex_file("hyginus.cex")

# Retrieve text content of a specific passage
ref = CtsUrn.from_string("urn:cts:latinLit:stoa1263.stoa001.hc:1pr.1")
psg = corpus.retrieve(ref)[0]
print(psg.text)
```

## Requirements

- Python >= 3.14
- pydantic
- urn-citation >= 0.4.1
- cite-exchange

## Development

### Running Tests


```bash
python -m unittest discover tests
```
or with `uv` from the project root:

```bash
uv run pytest
```


## License

See the LICENSE file for details.


## Related Projects

- [urn-citation](https://github.com/cite-architecture/urn_citation_py) - Python implementation of CTS URNs
- [cite-exchange](https://github.com/cite-architecture/cite_exchange_py) - Python library for CEX format

