import zipfile
import urllib.error
from unittest.mock import patch
import pandas as pd
import pytest
from util.data_util import read_csv, extract_zip_file, download_data

def test_read_csv_file_exists(tmp_path):
    """Test the `read_csv` function when the CSV file exists"""
    csv_path = tmp_path / "test.csv"
    df_tmp = pd.DataFrame({'col1': [1, 2, 3]})
    df_tmp.to_csv(csv_path, index=False)

    result = read_csv(csv_path)

    assert isinstance(result, pd.DataFrame)
    assert result.equals(df_tmp)
    assert result.columns.equals(df_tmp.columns)
    assert result.values[0] == df_tmp.values[0]


def test_read_csv_file_not_found():
    """ Test the `read_csv` function when the CSV file does not exist"""
    with pytest.raises(FileNotFoundError):
        read_csv("non_existent_path.csv")


def test_read_csv_empty_file(tmp_path):
    """Test the `read_csv` function with an empty CSV file"""
    empty_csv_path = tmp_path / "empty.csv"
    empty_csv_path.touch()

    with pytest.raises(pd.errors.EmptyDataError):
        read_csv(empty_csv_path)


def test_extract_zip_file_wrong_type(tmp_path):
    """Test the `extract_zip_file` function with an invalid zip file type"""
    invalid_zip_path = tmp_path / "invalid.tar.gz"
    invalid_zip_path.touch()

    with pytest.raises(zipfile.BadZipFile):
        extract_zip_file(invalid_zip_path, tmp_path)


def test_extract_zip_file_not_found(tmp_path):
    """Test the `extract_zip_file` function with a non-existent zip file"""
    with pytest.raises(FileNotFoundError):
        extract_zip_file("non_existent_path.zip", tmp_path)


def test_download_data_url_error(tmp_path):
    """Test the download_data function for handling a URL error"""
    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_urlopen.side_effect = urllib.error.URLError("Erro ao abrir a URL")

        with pytest.raises(urllib.error.URLError):
            download_data(tmp_path)
