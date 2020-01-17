"""Termania.net API client models."""

from sys import version_info

if version_info >= (3, 7):
    # Import dataclasses in Python 3.7 and above
    from .data_classes import Dictionary, EntryIndex, Entry
else:
    # Import namedtuples in Python 3.6 and less
    from .named_tuples import Dictionary, EntryIndex, Entry
