from random import choice
from urllib.parse import urljoin

import pytest
import simplejson as json

from termania.constants import BASE_URL


@pytest.fixture
def fake_entry_index_data(faker):
    return dict(
        absolute_index=faker.random_int(min=0, max=1_000_000, step=1),
        relative_index=faker.random_int(min=0, max=10, step=1),
        query=faker.word(),
        dictionary_id=faker.random_int(min=8, max=142, step=1),
    )


@pytest.fixture
def fake_entry_data(faker):
    headword = faker.word()
    entry_id = faker.random_int(min=0, max=1_000_000, step=1)
    dictionary_id = faker.random_int(min=8, max=142, step=1)
    xml = f"""<?xml version="1.0" encoding="utf-8"?><response xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://api.termania.net/1.0/get-entry/result"><dictionary_id>{dictionary_id}</dictionary_id><entry_id>{entry_id}</entry_id><headword>{headword}</headword><html_content><p xmlns="http://www.w3.org/1999/xhtml" xmlns:e="urn:STP_XMLDATA"><span class="color_orange font_xlarge strong">{headword} </span><span class="color_lightdark font_small italic">({faker.word()}) </span><span class="color_lightdark font_small">{faker.word()}, </span><span class="color_lightdark font_small">{choice(("m", "ž"))}. sp. </span><br /><br /><span class="italic font_small color_lightdark">Oblike: </span><span class="">{", ".join((faker.words(nb=faker.random_int(min=1, max=10))))} </span><hr style="color: #e3e3e3;background-color: #e3e3e3; height: 1px;border: 0 none;" /><span class=""><span class="italic font_small color_lightdark">Pomen: </span><span class="color_orange">{faker.word()} </span><br /><span class="italic font_small color_lightdark">Povezava spredaj: </span><span class="font_large">{", ".join((faker.words(nb=faker.random_int(min=1, max=4))))} </span><span class="color_lightdark font_small italic"><br />Angleški prevod: </span><span class="color_dark font_xlarge">{faker.word()}</span><span class="color_lightdark font_small italic"><br />Nemški prevod: </span><span class="color_dark font_xlarge">{faker.word()}</span>, <span class="color_dark font_xlarge">{faker.word()}</span><span class="color_lightdark font_small italic"><br />Albanski prevod: </span><span class="color_dark font_xlarge">{faker.word()}</span><span class="color_lightdark font_small italic"><br />Francoski prevod: </span><span class="color_dark font_xlarge">{faker.word()}</span></span><hr style="color: #e3e3e3;background-color: #e3e3e3; height: 1px;border: 0 none;" /><span class=""><span class="italic font_small color_lightdark">Pomen: </span><span class="color_orange">{faker.word()} </span><br /><span class="italic font_small color_lightdark">Povezava spredaj: </span><span class="font_large">{", ".join(faker.words(nb=faker.random_int(min=1, max=4)))} </span><span class="color_lightdark font_small italic"><br />Slovenska sopomenka: </span><span class="font_large">{faker.word()}</span><span class="color_lightdark font_small italic"><br />Angleški prevod: </span><span class="color_dark font_xlarge">{faker.word()}</span>, <span class="color_dark font_xlarge">{faker.word()}</span>, <span class="color_dark font_xlarge">{faker.word()}</span>, <span class="color_dark font_xlarge">{" ".join(faker.words(nb=2))}</span><span class="color_lightdark font_small italic"><br />Nemški prevod: </span><span class="color_dark font_xlarge">{faker.word()}</span><span class="color_lightdark font_small italic"><br />Francoski prevod: </span><span class="color_dark font_xlarge">{faker.word()}</span></span><hr style="color: #e3e3e3;background-color: #e3e3e3; height: 1px;border: 0 none;" /><span class=""><span class="italic font_small color_lightdark">Pomen: </span><span class="color_orange">{faker.word()} </span>(<span class="italic">{faker.word()}</span>)<span class="color_lightdark font_small italic"><br />Angleški prevod: </span><span class="color_dark font_xlarge">{faker.word()}</span></span><hr style="color: #e3e3e3;background-color: #e3e3e3; height: 1px;border: 0 none;" /><span class=""><span class="italic font_small color_lightdark">Pomen: </span><span class="color_orange">{faker.word()} </span>(<span class="italic">{" ".join(faker.words(nb=2))}</span>)<span class="color_lightdark font_small italic"><br />Angleški prevod: </span><span class="color_dark font_xlarge">{faker.word()}</span></span></p></html_content></response>"""
    return dict(
        headword=headword, entry_id=entry_id, dictionary_id=dictionary_id, xml=xml
    )


@pytest.fixture
def fake_dictionaries_data(faker):
    dictionaries = tuple(
        {
            "Author": faker.name(),
            "Id": n,
            "Name": " ".join(faker.words(nb=faker.random_int(min=2, max=7))),
            "Languages": tuple(
                faker.language_code() for _ in range(faker.random_int(min=2, max=5))
            ),
            "Lingualism": choice((1, 2)),
            "Type": 1,
        }
        for n in range(1, faker.random_int(min=2, max=100))
    )

    return {"Dictionaries": dictionaries, "Total": len(dictionaries)}


class RequestsHelpers:
    def __init__(self, requests_mock):
        self._requests_mock = requests_mock

    def mock_entry_index_request(self, data, status_code=200, raw_data=False):
        self._requests_mock.get(
            urljoin(BASE_URL, "search/entry-index"),
            text=json.dumps(
                {
                    "AbsoluteIndex": data["absolute_index"],
                    "RelativeIndex": data["relative_index"],
                }
            )
            if not raw_data
            else data,
            status_code=status_code,
        )

    def mock_entry_request(self, data, status_code=200, raw_data=False):
        self._requests_mock.get(
            urljoin(BASE_URL, "search/get-entry"),
            text=data["xml"] if not raw_data else data,
            status_code=status_code,
        )

    def mock_get_dictionaries(self, data, status_code=200, raw_data=False):
        self._requests_mock.get(
            urljoin(BASE_URL, "dictionary/list"),
            text=json.dumps(data) if not raw_data else data,
            status_code=status_code,
        )


@pytest.fixture
def requests_helpers(requests_mock):
    return RequestsHelpers(requests_mock)
