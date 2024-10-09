


import subprocess
import os
import pexpect
import time
from log.ycrash_logger import ycrash_logger

"""
Execute a system command and return its output and return code.

Args:
- command: str or list. The command to be executed. If it's a string, it will be passed to the shell for execution.

Returns:
- output: str. The output of the command.
"""
def run_command(command):
    try:
        if isinstance(command, str):
            output = subprocess.check_output(command, shell=True, universal_newlines=True)
        elif isinstance(command, list):
            output = subprocess.check_output(command, universal_newlines=True)
        else:
            raise ValueError("Invalid command type. Must be a string or list.")

        return_code = 0  # Success
    except subprocess.CalledProcessError as e:
        ycrash_logger.error(f" {command} failed with error {e.output} return_code {e.returncode}")
        output = f"Error while retriving for command {command} errorcode {e.returncode}"
        return_code = e.returncode
    return output.strip()

"""
    Get the current process ID (PID).

    Returns:
    - pid: int. The current process ID.
"""
def get_current_pid():
    return os.getpid()

"""
    Runs interactive commands, waits for the configured sleep time for the command to complete, and sends a carriage return to retrieve the system logs.
    Returns:
    - output: string. Runs the command output
"""
def run_interactive_command(command,sleeptime):
    # Run the 'top' command with the specified PID
    process = pexpect.spawn(command)
    time.sleep(sleeptime)
    process.send('\r')
    print(f"Carriaege retuurn")
    process.sendintr()
    output = ""
    try:
        # Capture output
        # output = process.read(size=5000).decode('utf-8')
        while True:
            chunk = process.read(100)
            output += chunk.decode('utf-8')
            if not chunk:
                break  # Reached EOF
    except pexpect.exceptions.TIMEOUT as e:
        print("Timeout exceeded while executing command:", command)
        return output
    # while True:
    # chunk = process.read(5000)
    #  if not chunk:
    #      break  # Reached EOF
    #   output += chunk.decode('utf-8')
    # print(f"read")

    # Return the captured output
    return output


"""
    Get the server API key from yCrash config

    Returns:
    - string. key from config file
"""
def getKey(config):
    return config.get('options', {}).get('k')


"""
    Get the server url  from yCrash config

    Returns:
    - string. url from config file
"""
def getServerUrl(config, endpoint):
    return config.get('options', {}).get('s') + endpoint
