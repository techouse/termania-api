import pytest
from bs4 import BeautifulSoup

from termania import API, Entry, Dictionary


class TestAPI:
    def test_search(
        self, requests_helpers, fake_entry_index_data, fake_entry_data, faker
    ):
        fake_entry_index_data["absolute_index"] = fake_entry_data["entry_id"]
        requests_helpers.mock_entry_index_request(fake_entry_index_data)
        requests_helpers.mock_entry_request(fake_entry_data)
        soup = BeautifulSoup(fake_entry_data["xml"], "lxml-xml")

        client = API(licence_key=faker.random_number(digits=7, fix_len=False))

        assert Entry(
            dictionary_id=fake_entry_data["dictionary_id"],
            entry_id=fake_entry_data["entry_id"],
            headword=fake_entry_data["headword"],
            html=soup.find("html_content").decode_contents(),
        ) == client.search(
            fake_entry_index_data["query"], fake_entry_index_data["dictionary_id"],
        )

    @pytest.mark.parametrize(
        "absolute_index,relative_index", [(1, -1), (-1, 1), (-1, -1)]
    )
    def test_search_no_results(
        self,
        requests_helpers,
        fake_entry_index_data,
        fake_entry_data,
        absolute_index,
        relative_index,
        faker,
    ):
        fake_entry_index_data["absolute_index"] = absolute_index
        fake_entry_index_data["relative_index"] = relative_index
        requests_helpers.mock_entry_index_request(fake_entry_index_data)
        requests_helpers.mock_entry_request(fake_entry_data)

        client = API(licence_key=faker.random_number(digits=7, fix_len=False))

        assert None is client.search(
            fake_entry_index_data["query"], fake_entry_index_data["dictionary_id"],
        )

    def test_get_dictionaries(self, requests_helpers, fake_dictionaries_data, faker):
        requests_helpers.mock_get_dictionaries(fake_dictionaries_data)

        client = API(licence_key=faker.random_number(digits=7, fix_len=False))

        assert {
            dictionary["Id"]: Dictionary(
                id=dictionary["Id"],
                name=dictionary["Name"],
                author=dictionary["Author"],
                languages=tuple(dictionary["Languages"]),
                lingualism=dictionary["Lingualism"],
                type=dictionary["Type"],
            )
            for dictionary in fake_dictionaries_data["Dictionaries"]
        } == client.get_dictionaries()

    def test_get_dictionaries_http_error(
        self, requests_helpers, fake_dictionaries_data, faker
    ):
        requests_helpers.mock_get_dictionaries(
            fake_dictionaries_data, status_code=faker.random_int(min=400, max=599)
        )

        client = API(licence_key=faker.random_number(digits=7, fix_len=False))

        assert None is client.get_dictionaries()

    def test_get_dictionaries_bad_data(
        self, requests_helpers, fake_dictionaries_data, faker
    ):
        requests_helpers.mock_get_dictionaries(faker.paragraph(), raw_data=True)

        client = API(licence_key=faker.random_number(digits=7, fix_len=False))

        assert None is client.get_dictionaries()
