# Usage
# python bigquery_update_parameterized_script.py \
# --sql_read_folder_path "./ddl/temp" \
# --sql_write_folder_path "./ddl/dev" \
# --param_string "edw=edw-dev-c119a7,supplychain=supplychain-dlf-dev-72acad"

import logging
import os
import sys


def update_parameters(file_name, path, param_dict, logger):
    """
    Function to update the Parameters in the given SQL file

    Args:
        file_name ([str]): [SQL File name]
        param_dict ([type]): [Parameter Config having all the Values]

    Returns:
        [Boolean]: [True if update is Successfull]
    """
    try:
        logger.debug("Reading SQL File %s", file_name)
        with open(file_name, "r") as sql_fh:
            sql = sql_fh.read()

        logger.debug(
            "Updating SQL \n%s with parameter Configuration %s",
            sql,
            param_dict,
        )
        updated_sql = sql
        for param in param_dict:
            updated_sql = updated_sql.replace(param, param_dict[param])

        if not os.path.exists(path):
            os.makedirs(path)
        write_file = os.path.join(path, os.path.split(file_name)[1])
        logger.debug(
            "Writing Updated SQL \n%s to file %s",
            updated_sql,
            write_file,
        )
        with open(write_file, "w") as sql_fh:
            sql_fh.write(updated_sql)
    except Exception as e:
        logger.warning("Unable to replace the parameter values.")
        logger.error(e)
        return False

    return True


def parse_parameter_string(param_string, logger):
    """
    Function to parse the Parameter string and convert it into a dictionary

    Args:
        param_string ([str]): [Parameter String]

    Returns:
        [Dict[Str, Str]]: [Dictionary with Parameter as key and value as value]
    """
    logger.debug("Got Parameters param_string: %s", param_string)
    param_dict = {}
    if param_string != "":
        params = [param.split("=", 1) for param in param_string.split(",")]
        for param in params:
            parameter = "{{" + param[0] + "}}"
            value = param[1]
            logger.debug(
                "Got value as %s for Parameter %s",
                value,
                parameter,
            )
            param_dict[parameter] = value

    return param_dict


def update_sql_files(read_path, write_path, param_string, logger):
    """
    Function to update the SQL Files with actual parameter values
    in the given Folder.

    Args:
        path ([str]): [Folder Path]
        param_string ([str]): [Parameter string with key values]
    """

    try:
        logger.debug(
            "Got Parameters read_path: %s, write_path: %s, param_string: %s",
            read_path,
            write_path,
            param_string,
        )
        param_dict = parse_parameter_string(param_string, logger)
        logger.info("Parsed Parameter Configuration is %s", param_dict)
        all_sql_files = find_sql_files(read_path, logger)
        path = read_path
        if not (write_path is None or write_path.strip() == ""):
            path = write_path
        for file in all_sql_files:
            if update_parameters(file, path, param_dict, logger):
                logger.info(
                    """Successfully replaced the parameters for %s and
                    written to %s""",
                    file,
                    path,
                )
            else:
                logger.warning(
                    "Unable to replace the parameters for %s",
                    file,
                )
    except Exception as e:
        logger.error("Got Exception.")
        logger.error(e)
        sys.exit("Unable to Update the SQL Files")

    return True


def find_sql_files(path, logger):
    """
    Find SQL files in the given path.
    Returns a list
    """
    logger.debug("Finding SQL files in %s", path)
    try:
        files = os.listdir(path)
    except OSError as err:
        logger.error("Error listing SQL directory %s: %s", path, err.strerror)
        return []
    sql_files = [
        os.path.join(path, entry)
        for entry in files
        if entry.endswith(".sql") and os.path.isfile(os.path.join(path, entry))
    ]
    sql_files.sort()
    logger.debug("Found SQL files: %s", ", ".join(sql_files))
    return sql_files


def get_logger(debug):
    """
    Function to create logger with INFO level

    Returns:
        [Logger]: [returns logger Object]
    """

    TS_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    if debug:
        logging.basicConfig(level=logging.DEBUG, format=TS_FORMAT)
    else:
        logging.basicConfig(level=logging.INFO, format=TS_FORMAT)
    return logging.getLogger("bigquery_update_parameterized_script")


def run_main_flow(ddl_read_folder_path: str, ddl_write_folder_path: str, param_string: str, debug: bool):
    print(
        "Processing files on the path: %s." % ddl_read_folder_path,
    )
    print("Parameters passed are: %s" % param_string)
    print(
        "Processed files will be stored on path: %s." % ddl_write_folder_path,
    )
    logger = get_logger(debug)
    return update_sql_files(ddl_read_folder_path, ddl_write_folder_path, param_string, logger)


def main():
    # setup vars
    ddl_read_folder_path = os.environ["INPUT_DDL_READ_FOLDER_PATH"]
    ddl_write_folder_path = os.environ["INPUT_DDL_WRITE_FOLDER_PATH"]
    param_string = os.environ["INPUT_PARAM_STRING"]
    debug = os.environ["INPUT_DEBUG"].lower() == "true"
    run_main_flow(ddl_read_folder_path, ddl_write_folder_path, param_string, debug)


if __name__ == "__main__":
    main()
