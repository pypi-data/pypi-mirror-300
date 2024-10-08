"""
    yCrash System Profiler: System Profiler
    This service is reponsible for retrieving and uploading system data to yCrash
"""
from datetime import datetime

from commons.common import run_command
from commons.webclient import upload_json_data
import json
from commons.common import getKey, getServerUrl
from .system_info import SystemInfo
from .system_commands import BaseCommands
from log.ycrash_logger import ycrash_logger


PS_DUMP_ENDPOINT = "/cm-receiver&dt=ps"
DF_DUMP_ENDPOINT = "/cm-receiver&dt=df"
NETSTAT_DUMP_ENDPOINT = "/cm-receiver&dt=ns"
KERNAL_DUMP_ENDPOINT = "/cm-receiver&dt=kernal"
TOP_DUMP_ENDPOINT = "/cm-receiver&dt=top"
TOPH_DUMP_ENDPOINT = "/cm-receiver&dt=toph"
DMSEG_DUMP_ENDPOINT = "/cm-receiver&dt=dmesg"
PING_DUMP_ENDPOINT = "/cm-receiver&dt=ping"
VMSTAT_DUMP_ENDPOINT = "/cm-receiver&dt=vmstat"


"""
    Runs all system commands for the OS.
"""
def export_all_system_data(config):
    system_info = SystemInfo()
    commands_manager = BaseCommands().get_commands(system_info.get_os_name())
    capture_and_upload_system_data(config, PS_DUMP_ENDPOINT, commands_manager.PS)
    capture_and_upload_system_data(config, DF_DUMP_ENDPOINT, commands_manager.Disk)
    capture_and_upload_system_data(config, NETSTAT_DUMP_ENDPOINT, commands_manager.NetStat)
    capture_and_upload_system_data(config, TOP_DUMP_ENDPOINT, commands_manager.Top)
    capture_and_upload_system_data(config, TOPH_DUMP_ENDPOINT, commands_manager.TopH)
    capture_and_upload_system_data(config, DMSEG_DUMP_ENDPOINT, commands_manager.DMesg2)
    capture_and_upload_system_data(config, KERNAL_DUMP_ENDPOINT, commands_manager.KernelParam)
    capture_and_upload_system_data(config, VMSTAT_DUMP_ENDPOINT, commands_manager.VMState)
    capture_and_upload_system_data(config, PING_DUMP_ENDPOINT, commands_manager.Ping)


"""
    Executes each system data and export the data to yCrash server
"""
def capture_and_upload_system_data(config, endpoint, command):
    start_time = datetime.now()
    data = {
        "data": run_command(command),
    }
    end_time = datetime.now()
    time_took = end_time - start_time
    system_details_json = json.dumps(data, indent=4)
    upload_json_data('application/json', getKey(config), getServerUrl(config, endpoint),
                     system_details_json)
    ycrash_logger.debug(f"Time taken for command {command} is {time_took.total_seconds()}")