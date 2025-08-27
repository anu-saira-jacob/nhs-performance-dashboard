import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db import fetch_df


# Test that fetch_df executes a query with parameters correctly
def test_fetch_df_with_params():
    # Create a fake DataFrame to be returned by pd.read_sql
    mock_df = pd.DataFrame({"col": [1, 2, 3]})

    # Patch both the SQLAlchemy connection and pandas.read_sql
    with patch("db.engine.connect") as mock_connect, \
         patch("pandas.read_sql", return_value=mock_df) as mock_read_sql:

        # Simulate the context manager for engine.connect()
        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn

        query = "SELECT * FROM test_table WHERE x = %(value)s"
        params = {"value": 5}

        result = fetch_df(query, params)

        # Check that read_sql was called with correct arguments
        mock_read_sql.assert_called_once_with(query, mock_conn, params=params)

        # Ensure the returned result is our mock DataFrame
        assert result.equals(mock_df)


# Test that fetch_df handles TypeError when params are None (fallback to no params)
def test_fetch_df_without_params_typeerror():
    mock_df = pd.DataFrame({"col": [10, 20]})

    with patch("db.engine.connect") as mock_connect, \
         patch("pandas.read_sql", side_effect=[TypeError("params issue"), mock_df]) as mock_read_sql:

        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn

        query = "SELECT * FROM another_table"

        result = fetch_df(query)  # No params passed here

        # It should have tried once with None (caused TypeError), then again without params
        assert mock_read_sql.call_count == 2
        call_args_1 = mock_read_sql.call_args_list[0][0]
        call_args_2 = mock_read_sql.call_args_list[1][0]

        # Confirm both calls used the same query and connection
        assert call_args_1[0] == call_args_2[0] == query
        assert result.equals(mock_df)


# Optional: Test that other exceptions (not TypeError) are not swallowed
def test_fetch_df_raises_other_errors():
    with patch("db.engine.connect") as mock_connect, \
         patch("pandas.read_sql", side_effect=ValueError("something went wrong")):

        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn

        with pytest.raises(ValueError, match="something went wrong"):
            fetch_df("SELECT * FROM faulty_query")
