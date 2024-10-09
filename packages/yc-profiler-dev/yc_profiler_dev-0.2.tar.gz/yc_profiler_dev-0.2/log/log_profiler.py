"""
    yCrash Python Profiler: Log Analyser
    This service responsible to extract the log changes and uploads to sever in chunks
"""

import os
import logging
import json
import time
from commons.webclient import upload_json_data
from commons.common import  getKey, getServerUrl
from .ycrash_logger import ycrash_logger


LOG_DUMP_ENDPOINT = "/cm-receiver+&dt=applog"
LOG_UPLOAD_LINES=100

"""
 Uploads the log changes to the server in chunks:
 - Log files are discovered or provided as arguments.
 - The log analyzer identifies the differences between backed-up and current log files.
"""
def upload_log_data(config):
    if config.get('options', {}).get('appLogs') is not None:
        log_path = config.get('options', {}).get('appLogs')
    else:
        log_path = get_log_file_location()

    logBackUpFile = log_path + '.ycrash.bak'
    if not os.path.exists(logBackUpFile):
        with open(logBackUpFile, 'w'):
            pass

    with open(log_path, 'r') as new_log_file:
        new_log_lines = set(new_log_file.readlines())

    with open(logBackUpFile, 'r') as old_log_file:
        old_log_lines = set(old_log_file.readlines())

    new_additions = new_log_lines - old_log_lines
    new_lines_list = list(new_additions)
    uploadInChunks(config, new_lines_list)
    copy_file(log_path, logBackUpFile)

"""
    Uploads the log  to the yCrash server in chunks
"""
def uploadInChunks(config, new_additions):
    for i in range(0, len(new_additions), LOG_UPLOAD_LINES):
        chunk_lines = new_additions[i:i + LOG_UPLOAD_LINES]
        log_lines = json.dumps(chunk_lines, indent=4)
        log_json = {
            "captureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "logs": log_lines
        }

        ycrash_logger.debug("Uploading app logs...")
        # Upload log_json
        upload_json_data('application/json', getKey(config), getServerUrl(config, LOG_DUMP_ENDPOINT),
                         json.dumps(log_json, indent=4))

        # Make a backup of the log file after uploading each chunk


"""
    Retrieves log file location from logger
    Returns:
    -  str. The absolute path of the 
"""
def get_log_file_location():
    # Get the root logger
    root_logger = logging.getLogger()

    # Iterate over all handlers of the root logger
    for handler in root_logger.handlers:
        # Check if the handler is a FileHandler
        if isinstance(handler, logging.FileHandler):
            # Return the log file's absolute path
            return handler.baseFilename

    # If no FileHandler is found, return None or any other value you prefer
    return None

"""
    Copies aall the source to the destinations
    - used to backup log file
"""
def copy_file(source_file, destination_file):
    try:
        # Open the source file in binary mode for reading
        with open(source_file, 'rb') as src_file:
            # Open the destination file in binary mode for writing
            with open(destination_file, 'wb') as dest_file:
                # Read the content of the source file and write it to the destination file
                dest_file.write(src_file.read())
        ycrash_logger.debug("yCrash log backup file copied successfully.")
    except FileNotFoundError:
        ycrash_logger.error("File not found.")
    except Exception as e:
        ycrash_logger.error(f"An error occurred: {e}")

"""
    Retrieves all the loggers to the logging module
    Returns:
    -  list of str. The absolute path of all the attached logger to the python module.
"""
def get_all_loggers():
    root_logger = ycrash_logger.getLogger()
    all_loggers = [root_logger]

    for logger_name in ycrash_logger.Logger.manager.loggerDict.keys():
        logger = logging.getLogger(logger_name)
        if logger.parent is root_logger:
            all_loggers.append(logger)

    return all_loggers
