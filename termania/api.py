"""Termania.net API client."""

from typing import Dict, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from termania.constants import BASE_URL
from termania.models import Dictionary, Entry, EntryIndex


class API:
    """Termania.net API client class."""

    def __init__(self, licence_key: int):
        """Set up a Requests session with the appropriate licence key."""
        self.api = requests.Session()
        self.api.headers.update(
            # unless explicitly set to JSON the API will return XML
            {"accept": "application/json"}
        )
        if not licence_key:
            raise ValueError("Invalid licence key!")
        self.api.params.update({"licenceKey": licence_key})

    def get_dictionaries(self) -> Optional[Dict[int, Dictionary]]:
        """Get a dictionary of dictionaries."""
        res = self.api.get(urljoin(BASE_URL, "dictionary/list"))
        if 200 <= res.status_code < 300:
            try:
                data = res.json()
                return {
                    dictionary["Id"]: Dictionary(
                        id=dictionary["Id"],
                        name=dictionary["Name"],
                        author=dictionary["Author"],
                        languages=tuple(dictionary["Languages"]),
                        lingualism=dictionary["Lingualism"],
                        type=dictionary["Type"],
                    )
                    for dictionary in data["Dictionaries"]
                }
            except (ValueError, KeyError):
                return None
        return None

    def search(self, query: str, dictionary_id: int) -> Optional[Entry]:
        """Search the Termania.net API for a query in a particular dictionary."""
        entry_index = self._get_entry_index(query, dictionary_id)
        if (
            entry_index  # pylint: disable=C0330
            and entry_index.absolute_index > -1  # pylint: disable=C0330
            and entry_index.relative_index > -1  # pylint: disable=C0330
        ):
            return self._get_entry(entry_index.absolute_index, dictionary_id)
        return None

    def _get_entry_index(self, query: str, dictionary_id: int) -> Optional[EntryIndex]:
        """Get the EntryIndex from the Termania.net API."""
        res = self.api.get(
            urljoin(BASE_URL, "search/entry-index"),
            params={"dictionaryId": dictionary_id, "query": query, "headword": query},
        )
        if 200 <= res.status_code < 300:
            try:
                data = res.json()
                return EntryIndex(
                    absolute_index=int(data["AbsoluteIndex"]),
                    relative_index=int(data["RelativeIndex"]),
                    query=query,
                    dictionary_id=dictionary_id,
                )
            except ValueError:
                return None
        return None

    def _get_entry(self, entry_id: int, dictionary_id: int) -> Optional[Entry]:
        """Get the Entry from the Termania.net API."""
        res = self.api.get(
            urljoin(BASE_URL, "search/get-entry"),
            params={"dictionaryId": dictionary_id, "entryId": entry_id},
            headers={
                # explicitly request XML instead of JSON
                "accept": "application/xml"
            },
        )
        if 200 <= res.status_code < 300:
            try:
                soup = BeautifulSoup(res.text, "html.parser")
                return Entry(
                    dictionary_id=int(soup.find("dictionary_id").get_text().strip()),
                    entry_id=int(soup.find("entry_id").get_text().strip()),
                    headword=soup.find("headword").get_text().strip(),
                    html=soup.find("html_content").decode_contents(),
                )
            except (TypeError, AttributeError):
                return None
        return None
