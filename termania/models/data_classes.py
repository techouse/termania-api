"""DataClasses as modules."""

from dataclasses import dataclass


@dataclass
class EntryIndex:
    """EntryIndex DataClass module."""

    absolute_index: int
    relative_index: int
    query: str
    dictionary_id: int


@dataclass
class Entry:
    """Entry DataClass module."""

    dictionary_id: int
    entry_id: int
    headword: str
    html: str


@dataclass
class Dictionary:
    """Dictionary DataClass module."""

    id: int  # pylint: disable=C0103
    name: str
    author: str
    languages: tuple
    lingualism: int
    type: int
