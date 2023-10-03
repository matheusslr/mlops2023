import pytest
import pandas as pd
from util.data_util import read_csv

def test_read_csv_file_exists(tmp_path):
    csv_path = tmp_path / "test.csv"
    df = pd.DataFrame({'col1': [1, 2, 3]})
    df.to_csv(csv_path, index=False)

    result = read_csv(csv_path)
    
    assert isinstance(result, pd.DataFrame)
    assert result.equals(df)
    assert result.columns.equals(df.columns)
    assert result.values[0] == df.values[0]

def test_read_csv_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_csv("non_existent_path.csv")

def test_read_csv_empty_file(tmp_path):
    empty_csv_path = tmp_path / "empty.csv"
    empty_csv_path.touch()

    with pytest.raises(pd.errors.EmptyDataError):
        read_csv(empty_csv_path)
