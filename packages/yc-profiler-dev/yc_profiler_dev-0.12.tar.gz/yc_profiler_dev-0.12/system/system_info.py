"""
    yCrash System Profiler: System information
"""
import platform

class SystemInfo:
    def __init__(self):
        self.os_name = platform.system()
        self.architecture = platform.architecture()[0]

    def get_os_name(self):
        return self.os_name

    def get_architecture(self):
        return self.architecture


