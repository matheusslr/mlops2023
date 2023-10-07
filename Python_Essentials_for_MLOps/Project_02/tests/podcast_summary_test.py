import os
import requests
from unittest.mock import Mock, patch
import pytest

from base_functions.podcast_functions import get_episodes, download_episodes

@patch('base_functions.podcast_functions.requests.get')
def test_get_episodes_successful(mock_get):
    mock_response = Mock()
    mock_response.text = """<rss version="2.0">
        <channel>
            <item>Episode 1</item>
            <item>Episode 2</item>
        </channel>
    </rss>"""
    mock_get.return_value = mock_response

    episodes = get_episodes()

    assert len(episodes) == 2
    assert episodes == ['Episode 1', 'Episode 2']


@patch('base_functions.podcast_functions.requests.get')
def test_get_episodes_http_error(mock_get):
    mock_get.side_effect = requests.exceptions.HTTPError("HTTP Error")

    with pytest.raises(requests.exceptions.HTTPError):
        get_episodes()

@patch('base_functions.podcast_functions.requests.get')
def test_get_episodes_timeout_error(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout("Timeout Error")

    with pytest.raises(requests.exceptions.Timeout):
        get_episodes()

@patch('base_functions.podcast_functions.requests.get')
def test_get_episodes_connection_error(mock_get):
    mock_get.side_effect = requests.exceptions.ConnectionError("Connection Error")

    with pytest.raises(requests.exceptions.ConnectionError):
        get_episodes()


@patch('os.path.exists')
@patch('base_functions.podcast_functions.requests.get')
def test_download_episodes(mock_requests_get, mock_os_path_exists):
    mock_response = Mock()
    mock_response.content = b"Mocked audio content"
    mock_requests_get.return_value = mock_response

    episodes = [
        {
            "link": "https://example.com/episode1",
            "enclosure": {
                "@url": "https://example.com/episode1.mp3"
            }
        },
        {
            "link": "https://example.com/episode2",
            "enclosure": {
                "@url": "https://example.com/episode2.mp3"
            }
        }
    ]

    audio_files = download_episodes(episodes)

    assert mock_os_path_exists.call_count == 2

    assert not isinstance(audio_files, None.__class__)

    assert len(audio_files) == 2
    assert audio_files[0]["link"] == "https://example.com/episode1"
    assert audio_files[1]["link"] == "https://example.com/episode2"

@patch('base_functions.podcast_functions.requests.get')
def test_download_episodes_timeout_error(mock_requests_get):
    mock_requests_get.side_effect = requests.exceptions.Timeout("Timeout Error")

    episodes = [
        {
            "link": "https://example.com/episode1",
            "enclosure": {
                "@url": "https://example.com/episode1.mp3"
            }
        }
    ]

    with pytest.raises(requests.exceptions.Timeout):
        download_episodes(episodes)

@patch('base_functions.podcast_functions.requests.get')
def test_download_episodes_connection_error(mock_requests_get):
    mock_requests_get.side_effect = requests.exceptions.ConnectionError("Connection Error")

    episodes = [
        {
            "link": "https://example.com/episode1",
            "enclosure": {
                "@url": "https://example.com/episode1.mp3"
            }
        }
    ]

    with pytest.raises(requests.exceptions.ConnectionError):
        download_episodes(episodes)