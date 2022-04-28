import logging
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, "../src")
from src import bigquery_update_parameterized_script


@pytest.fixture(autouse=True)
def mock_print(mocker):
    yield


@pytest.fixture()
def test_read_data_dir():
    yield os.path.relpath(Path(__file__).resolve().parent / "input")


@pytest.fixture()
def test_write_data_dir():
    yield os.path.relpath(Path(__file__).resolve().parent / "output")


@pytest.fixture()
def param_string_single():
    yield "PROJECT_ID=TEST_PROJECT"


# @pytest.fixture()
# def param_string_multiple():
#     yield "P1_PROJECT_ID=TEST_1_PROJECT,P2_PROJECT_ID=TEST_2_PROJECT,P3_PROJECT_ID=TEST_3_PROJECT"


@pytest.fixture()
def get_logger():
    TS_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=TS_FORMAT)
    return logging.getLogger("bigquery_update_parameterized_script")


def test_bigquery_parameterized_script(
    test_read_data_dir, test_write_data_dir, param_string_single, get_logger
):
    """Process input and check result."""
    return_code = bigquery_update_parameterized_script.run_main_flow(
        test_read_data_dir, test_write_data_dir, param_string_single, get_logger
    )
    if return_code == True:
        assert True
    else:
        assert False


def test_file_content():
    """check result/output of the main_flow and compare"""
    output = """CREATE OR REPLACE VIEW
  output.table_name
 AS
SELECT
	 column_name_1 as cn_1
	,column_name_2 as cn_2
	,column_name_3 as cn_3
	,column_name_4 as cn_4
	,column_name_5 as cn_5
	,column_name_6 as cn_6
	,column_name_7 as cn_7
	,created_datetime
	,modified_datetime
FROM
  `TEST_PROJECT.database.table_name`
"""
    if output == open("./tests/output/test_ddl.sql").read():
        assert True
    else:
        assert False
