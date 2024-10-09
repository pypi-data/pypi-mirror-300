"""
    yCrash Python Profiler: Process Analyser
    This service responsible to extract the process details and uploads the data to sever
"""

import psutil
import json
from commons.common import get_current_pid
from commons.webclient import upload_json_data
from commons.common import  getKey, getServerUrl
import getpass
import logging
import socket
from datetime import datetime
import time
import os
import sys

from log.ycrash_logger import ycrash_logger

PROCESS_DUMP_ENDPOINT = "/yc-receiver?dt=meta"

"""
    Retrieves and uploads the process details to the yCrash server
"""
def capture_print_process_details(config):
    try:
        process = psutil.Process(get_current_pid())
        process_data = {
            "pid": get_current_pid(),
            "host_name" : socket.gethostname(),
            "who_am_i": getpass.getuser(),
            "cpu_count": os.cpu_count(),
            "python_version": sys.version,
            "cpu_percent": process.cpu_percent(interval=1),
            "memory_info": process.memory_info()._asdict(),
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H-%M-%S"),
            "timezone": get_system_timezone(),
            "connections": len(process.connections()),
            "threads_count": len(process.threads()) # Count the number of threads
        }
        process_details = {"process_details": process_data}
        json_data = json.dumps(process_details, indent=4)
        ycrash_logger.debug("Uploading process logs...")
        upload_json_data('application/json', getKey(config), getServerUrl(config,PROCESS_DUMP_ENDPOINT), json_data)
    except psutil.NoSuchProcess:
        logging.error(f"Process with PID {get_current_pid()} not found.")
    except Exception as e:
        logging.error(f"Error: {e}")

"""
    Retrieves the IO details
"""
def get_io_details(io_counter):
    try:
        # Create a dictionary with I/O details
        io_dict = {
            "read_count": io_counter.read_count,
            "write_count": io_counter.write_count,
            "read_bytes": io_counter.read_bytes,
            "write_bytes": io_counter.write_bytes
        }
        # Convert the dictionary to a JSON-formatted string
        io_json = json.dumps(io_dict, indent=4)
        return io_json
    except psutil.Error as e:
        # Handle potential exceptions from psutil
        print(f"Error getting I/O details: {e}")
        return None

"""
    Returns the thread CPU usage percentage
"""
def get_threads_cpu_percent(p):
    threadList = []
    for thread in p.threads():
        total_percent = p.cpu_percent(0.1)
        total_time = sum(p.cpu_times())
        cpu_percentage = total_percent * ((thread.system_time + thread.user_time) / total_time)
        process_data = {'id': thread.id,
                        'cpu_percentage': cpu_percentage}

        threadList.append(process_data)
    return threadList

"""
    Retrieves the system timezone
"""
def get_system_timezone():
    # Get the timezone offset in seconds
    timezone_offset_seconds = time.timezone

    # Convert the offset to hours and minutes
    hours = abs(timezone_offset_seconds) // 3600
    minutes = (abs(timezone_offset_seconds) % 3600) // 60

    # Determine the sign of the timezone offset
    sign = '+' if timezone_offset_seconds >= 0 else '-'

    # Format the timezone information
    timezone_info = f"UTC{sign}{hours:02d}:{minutes:02d}"

    return timezone_info
