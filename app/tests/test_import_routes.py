from http import HTTPStatus
from .constants import (
    IMPORT_VALID_CATEGORY,
    INVALID_CATEGORY,
    VALID_YEAR,
    INVALID_YEAR_LOW,
    INVALID_YEAR_HIGH,
    BASE_IMPORT_URL,
)

def test_get_import_data_valid(client):
    response = client.get(f"{BASE_IMPORT_URL}/{IMPORT_VALID_CATEGORY}/{VALID_YEAR}")
    assert response.status_code in [HTTPStatus.OK, HTTPStatus.NO_CONTENT]
    data = response.json()
    if response.status_code == HTTPStatus.OK:
        assert isinstance(data, list)
        assert all("country" in item for item in data)
        assert all("amount" in item for item in data)
        assert all("value" in item for item in data)


def test_get_import_data_invalid_category(client):
    response = client.get(f"{BASE_IMPORT_URL}/{INVALID_CATEGORY}/{VALID_YEAR}")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "Invalid category" in response.json()["detail"]


def test_get_import_data_invalid_year_low(client):
    response = client.get(f"{BASE_IMPORT_URL}/{IMPORT_VALID_CATEGORY}/{INVALID_YEAR_LOW}")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "Year out of range" in response.json()["detail"]


def test_get_import_data_invalid_year_high(client):
    response = client.get(f"{BASE_IMPORT_URL}/{IMPORT_VALID_CATEGORY}/{INVALID_YEAR_HIGH}")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "Year out of range" in response.json()["detail"]


def test_get_all_import_data(client):
    response = client.get(f"{BASE_IMPORT_URL}/all", params={"offset": 0, "limit": 10})
    assert response.status_code in [HTTPStatus.OK, HTTPStatus.NO_CONTENT]
    data = response.json()
    if response.status_code == HTTPStatus.OK:
        assert isinstance(data, list)
        assert all("country" in item for item in data)
        assert all("amount" in item for item in data)
        assert all("value" in item for item in data)
        assert all("category" in item for item in data)
        assert all("year" in item for item in data)
