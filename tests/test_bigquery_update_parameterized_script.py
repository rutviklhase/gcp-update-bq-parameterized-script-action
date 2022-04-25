import logging
from pathlib import Path
from unittest import mock
from unittest.mock import patch
import sys
sys.path.insert(0, '../src')
import dataclasses
import pytest
import requests_mock
from types import SimpleNamespace

import bigquery_update_parameterized_script


@pytest.fixture(autouse=True)
def mock_print(mocker):
    yield


@pytest.fixture()
def test_read_data_dir():
    yield Path(__file__).resolve().parent / 'data'


@pytest.fixture()
def test_write_data_dir():
    TEST_WRITE_DATA_DIR = Path.tmp_path / "dev"
    yield  TEST_WRITE_DATA_DIR.mkdir()


@pytest.fixture()
def param_string_single():
    yield "PROJECT_ID=TEST_PROJECT"


@pytest.fixture()
def param_string_multiple():
    yield "P1_PROJECT_ID=TEST_1_PROJECT,P2_PROJECT_ID=TEST_2_PROJECT,P3_PROJECT_ID=TEST_3_PROJECT"


@pytest.fixture()
def test_get_logger():
    TS_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=TS_FORMAT)
    return logging.getLogger("bigquery_update_parameterized_script")

class TestBQUpdateParameterizedScript:
    def test_bigquery_parameterized_script(self, mocker, test_read_data_dir, test_write_data_dir, param_string_single, param_string_multiple, get_logger):
        """Process input and check result."""
        mock_find_sql_files = mocker.patch("src.bigquery_update_parameterized_script.find_sql_files")
        assert mock_find_sql_files.assert_called_once_with(test_read_data_dir,get_logger)

