import pytest
import requests

from unittest.mock import Mock, patch
from scraping import get_html_from_url, get_match_shooting_stats


def test_valid_url():
    url = "https://www.example.com"
    response = get_html_from_url(url)
    assert isinstance(response, requests.Response)
    assert response.status_code == 200


@patch("scraping.requests.get")
def test_http_error(mock_get):
    mock_get.side_effect = requests.exceptions.HTTPError("HTTP Error")
    with pytest.raises(requests.HTTPError):
        get_html_from_url("http://example.com/404")


@patch("scraping.requests.get")
def test_timeout_error(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout
    with pytest.raises(requests.Timeout):
        get_html_from_url("https://www.example.com", timeout=0.01)


@patch("scraping.requests.get")
def test_connection_error(mock_get):
    mock_get.side_effect = requests.exceptions.ConnectionError
    with pytest.raises(requests.ConnectionError):
        get_html_from_url("http://nonexistenturl123456789.com")

