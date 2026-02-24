# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## 0.3.0 - 2026-02-24

## Breaking changes

- in `CitablePassage` and `CitableCorpus` classes, the method `from_string` has been renamed to `from_delimited`

## Added

- new methods `cex` in the `CitablePassage` and `CitableCorpus` classes to serialize objects to CEX delimited-text format



## 0.2.0 - 2026-02-21 

### Added

- adds the `MarkupReader` abstract class, and the concrete `TEIDivAbReader` implementation to create citable corpora from XML documents
- adds the `EditionBuilder` abstract class, and the concrete `TEIDiplomatic` and `TEINormalized` implementations to create markup-free diplomatic and normalized editions from citable XML editions


## 0.1.0 - 2026-01-15 

Initial release.

### Added

- `CtsPassage` class to represent a citable passage of text and methods for creating passages from delimited strings.
- `CitableCorpus` class to represent a collection of passages, methods to create a `CitableCorpus` from CEX files and URLs.
- URN-based retrieval of passages from a corpus, including support for passage ranges.
- Documentation and usage examples in the README.

