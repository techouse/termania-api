"""Termania API models."""

from collections import namedtuple

EntryIndex = namedtuple(
    "EntryIndex", ["absolute_index", "relative_index", "query", "dictionary_id"]
)

Entry = namedtuple("Entry", ["dictionary_id", "entry_id", "headword", "html"])

Dictionary = namedtuple(
    "Dictionary", ["id", "name", "author", "languages", "lingualism", "type"]
)