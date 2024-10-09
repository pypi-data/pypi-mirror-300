"""
    yCrash Python Profiler: Profiler
    Main profiler service reads yCrash config, collected data and uploads to yCrash server
"""

import time
import threading
from threads.thread_profiler import capture_export_thread_data
from heap.heap_dump_profiler import HeapDumpCapturer
from process.process_profiler import capture_print_process_details
from gcprofiler.gc_profiler import ycrash_memory_extract
from log.log_profiler import upload_log_data
from system.system_profiler import export_all_system_data
from commons.webclient import upload_json_data
from commons.common import  getKey, getServerUrl
import yaml
import json
from log.ycrash_logger import ycrash_logger
from datetime import datetime


YC_FIN_ENDPOINT = "/yc-fin"


"""
    yCrash init - Routine to be called from external programs
    Runs a background thread to upload data.
"""

def ycrash_init(configFilePath):
    thread_states_thread = threading.Thread(target=profile_data, args=(configFilePath), name="yCrash.analyzer")
    thread_states_thread.start()

"""
    Profiler reads the config and calls data collection and uploads
"""
def profile_data(configFilePath):

    # Calculate the time taken

    ycrashConfig = load_config(configFilePath)
    ycrash_logger.debug("Loaded config file...")
    # gc.set_debug(gc.DEBUG_LEAK)
    # while True:
    start_time = datetime.now()

    ycrash_memory_extract(ycrashConfig)
    capture_export_thread_data(ycrashConfig)
    capturer = HeapDumpCapturer()
    capturer.capture_heap_dump(ycrashConfig)

    upload_log_data(ycrashConfig)
    capture_print_process_details(ycrashConfig)
    export_all_system_data(ycrashConfig)

    submit_fin(start_time, ycrashConfig)

        # time.sleep(ycrashConfig.get('options', {}).get('m3Frequency'))

"""
    Submits a fin after data is uploaded to the server
"""
def submit_fin(start_time, ycrashConfig):
    end_time = datetime.now()
    time_took = end_time - start_time
    time_taken = {
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "time_taken(seconds)": time_took.total_seconds()
    }
    time_json = json.dumps(time_taken, indent=4)
    upload_json_data('application/json', getKey(ycrashConfig), getServerUrl(ycrashConfig, YC_FIN_ENDPOINT), time_json)
    return time

"""
    Loads and parses yCrash config file 
"""
def load_config(configFilePath):
    try:
        ycrash_logger.debug("Loading config file...")

        # Read the YAML file
        with open(configFilePath, 'r') as file:
            print(file)
            data = yaml.safe_load(file)
        # Accessing attributes
        version = data.get('version')
        options = data.get('options', {})

        # Accessing specific attributes within options
        k = options.get('k')
        s = options.get('s')
        a = options.get('a')
        m3Frequency = options.get('m3Frequency')
        app_logs = options.get('appLogs', [])

        # Outputting the values
        ycrash_logger.debug(f"Version:{version}")
        # ycrash_logger.debug("key:", k)
        ycrash_logger.debug(f"Server(s): {s}")
        ycrash_logger.debug(f"Application(a): {a}")
        ycrash_logger.debug(f"Monitoring Frequency(m3Frequency): {m3Frequency}")

    except FileNotFoundError:
        ycrash_logger.error(f"yCrash agent config {configFilePath} not found")
        raise ValueError("yCrash agent config {configFilePath} not found")

    except yaml.YAMLError as exc:
        ycrash_logger.error("yCrash agent config parsing error")
        raise ValueError("yCrash agent config parsing error")
    return data


"""
    Validates yCrash config file 
"""
def check_config(version, k, s, a, m3Frequency):
    if not version:
        ycrash_logger.error(f"yCrash agent config Version field is empty or null")
        raise ValueError("Version field is empty or null")
    if not k:
        ycrash_logger.error(f"yCrash agent config k (key) field is empty or null")
        raise ValueError(f"yCrash agent config k (key) field is empty or null")
    if not s:
        ycrash_logger.error(f"yCrash agent config s (server url) field is empty or null")
        raise ValueError("yCrash agent config s (server url) field is empty or null")
    if not a:
        ycrash_logger.error(f"yCrash agent config a (application name) field is empty or null")
        raise ValueError(f"yCrash agent config a (application name) field is empty or null")
    if not m3Frequency:
        ycrash_logger.error(f"yCrash agent config m3Frequency field is empty or null")
        raise ValueError(f"yCrash agent config m3Frequency field is empty or null")




