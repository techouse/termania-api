import pytest
from bs4 import BeautifulSoup

from termania import API, EntryIndex, Entry


class TestAPI:
    def test_invalid_init(self):
        with pytest.raises(TypeError) as excinfo:
            API()
        assert "missing 1 required positional argument: 'licence_key'" in str(
            excinfo.value
        )

    def test_invalid_licence_key(self):
        with pytest.raises(ValueError) as excinfo:
            API(licence_key=None)
        assert "Invalid licence key!" in str(excinfo.value)

    def test_get_entry_index(self, requests_helpers, fake_entry_index_data, faker):
        requests_helpers.mock_entry_index_request(fake_entry_index_data)

        client = API(licence_key=faker.random_number(digits=7, fix_len=False))

        assert EntryIndex(**fake_entry_index_data) == client._get_entry_index(
            fake_entry_index_data["query"],
            fake_entry_index_data["dictionary_id"],
        )

    def test_get_entry_index_http_error(
        self, requests_helpers, fake_entry_index_data, faker
    ):
        requests_helpers.mock_entry_index_request(
            fake_entry_index_data, status_code=faker.random_int(min=400, max=599)
        )

        client = API(licence_key=faker.random_number(digits=7, fix_len=False))

        assert None is client._get_entry_index(
            fake_entry_index_data["query"],
            fake_entry_index_data["dictionary_id"],
        )

    def test_get_entry_index_bad_data(
        self, requests_helpers, fake_entry_index_data, faker
    ):
        requests_helpers.mock_entry_index_request(faker.paragraph(), raw_data=True)

        client = API(licence_key=faker.random_number(digits=7, fix_len=False))

        assert None is client._get_entry_index(
            fake_entry_index_data["query"],
            fake_entry_index_data["dictionary_id"],
        )

    def test_get_entry(self, requests_helpers, fake_entry_data, faker):
        requests_helpers.mock_entry_request(fake_entry_data)

        client = API(licence_key=faker.random_number(digits=7, fix_len=False))

        soup = BeautifulSoup(fake_entry_data["xml"], "lxml-xml")

        assert Entry(
            dictionary_id=fake_entry_data["dictionary_id"],
            entry_id=fake_entry_data["entry_id"],
            headword=fake_entry_data["headword"],
            html=soup.find("html_content").decode_contents(),
        ) == client._get_entry(
            fake_entry_data["entry_id"], fake_entry_data["dictionary_id"]
        )

    def test_get_entry_http_error(self, requests_helpers, fake_entry_data, faker):
        requests_helpers.mock_entry_request(
            fake_entry_data, status_code=faker.random_int(min=400, max=599)
        )

        client = API(licence_key=faker.random_number(digits=7, fix_len=False))

        assert None is client._get_entry(
            fake_entry_data["entry_id"], fake_entry_data["dictionary_id"]
        )

    def test_get_entry_bad_data(self, requests_helpers, fake_entry_data, faker):
        requests_helpers.mock_entry_request(faker.paragraph(), raw_data=True)

        client = API(licence_key=faker.random_number(digits=7, fix_len=False))

        assert None is client._get_entry(
            fake_entry_data["entry_id"], fake_entry_data["dictionary_id"]
        )
