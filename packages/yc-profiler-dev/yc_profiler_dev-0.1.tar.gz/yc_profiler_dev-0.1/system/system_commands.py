"""
    yCrash System Profiler: Encapsulates all the system commands
"""

from log.ycrash_logger import ycrash_logger
import os

PING_ENDPOINT = "google.com"


"""
    Base command class containing system commands
"""
class BaseCommands:
    def __init__(self, NetStat="netstat -an", PS="ps -ef", PS2="ps -ef", M3PS="ps -ef", Disk="df -hk",
                 Top="top -l 5 && sleep 10", Top2="", TopH="top -l 1 -pid {os.getpid()}", TopH2="",
                 Top4M3="top -l 1", VMState="vm_stat -c 10 5", DMesg="dmesg",
                 DMesg2="cat /var/log/system.log | tail -20", ProcessTopCPU="ps -eo pid,command,%cpu -r",
                 ProcessTopMEM="ps -eo pid,command,%mem -m", OSVersion="uname -a", KernelParam="sysctl -a",
                 Ping=f"ping -c 6 {PING_ENDPOINT}", SHELL="/bin/sh -c"):
        self.NetStat = NetStat
        self.PS = PS
        self.PS2 = PS2
        self.M3PS = M3PS
        self.Disk = Disk
        self.Top = Top
        self.Top2 = Top2
        self.TopH = TopH
        self.TopH2 = TopH2
        self.Top4M3 = Top4M3
        self.VMState = VMState
        self.DMesg = DMesg
        self.DMesg2 = DMesg2
        self.ProcessTopCPU = ProcessTopCPU
        self.ProcessTopMEM = ProcessTopMEM
        self.OSVersion = OSVersion
        self.KernelParam = KernelParam
        self.Ping = Ping
        self.SHELL = SHELL

    """
        Get the system commands object on the os type
    """
    def get_commands(self,os_type):
        ycrash_logger.debug(f"os_type: {os_type}")
        if os_type == "Darwin":
            return DarwinCommands()
        elif os_type == "Linux":
            return LinuxCommands()
        elif os_type == "Solaris":
            return SolarisCommands()
        elif os_type == "Windows":
            return WindowsCommands()
        elif os_type == "AIX":
            return AIXCommands()
        else:
            raise NotImplementedError(f"OS type '{os_type}' not supported.")
"""
    Darwin(mac) command class containing system commands
"""
class DarwinCommands(BaseCommands):
    def __init__(self):
        super().__init__(
            NetStat="netstat -an",
            PS="ps -ef",
            PS2="ps -ef",
            M3PS="ps -ef",
            Disk="df -hk",
            Top="for i in {1..3}; do top -l 5 ; sleep 10; done",
            Top2="",  # Placeholder for no operation
            TopH=f"top -l 1 -pid {os.getpid()}",
            TopH2="",  # Placeholder for no operation
            Top4M3="top -l 1",
            VMState="vm_stat -c 10 5",
            DMesg="dmesg",
            DMesg2="cat /var/log/system.log | tail -20",
            ProcessTopCPU="ps -eo pid,command,%cpu -r",
            ProcessTopMEM="ps -eo pid,command,%mem -m",
            OSVersion="uname -a",
            KernelParam="sysctl -a",
            Ping=(f"ping -c 6 {PING_ENDPOINT}"),
            SHELL="/bin/sh -c"
        )
"""
    Linux command class containing system commands
    TODO -  Untested
"""
class LinuxCommands(BaseCommands):
    def __init__(self):
        super().__init__(
            NetStat="netstat -pan",
            PS="ps -eLf",
            PS2="ps -eTf",
            M3PS="ps -eLf",
            Disk="df -hk",
            Top="top -bc -d 10 -n 3",
            Top2="Executable() -topMode -bc -d 10 -n 3",
            TopH="top -bH -n 1 -p {DynamicArg}",
            TopH2="Executable() -topMode -bH -n 1 -p",
            Top4M3="Executable() -topMode -bc -n 1",
            #  TOCHECK - What is the TOP_INTERVAL is the frequency ? and what is script span
            # VMState="vmstat {DynamicArg} {DynamicArg} | awk '{{cmd=\"(date +'\\''%H:%M:%S'\\'' )\"; cmd | getline now; print now $0; fflush(); close(cmd)}}'",
            DMesg="dmesg -T --level=emerg,alert,crit,err,warn | tail -20",
            DMesg2="dmesg --level=emerg,alert,crit,err,warn | tail -20 | awk '{{gsub(/\\\\[[^]]*\\\\]/,\"\"); print strftime(\"[%%a %%b %%d %%H:%%M:%%S %%Y]\", systime()-$(NF-1)), $0}}'",
            ProcessTopCPU="ps -o pid,%cpu,cmd,ax | sort -b -k2 -r",
            ProcessTopMEM="ps -o pid,%mem,cmd,ax | sort -b -k2 -r",
            OSVersion="uname -a",
            KernelParam="sysctl -a",
            Ping=f"ping -c 6 {PING_ENDPOINT}",
            SHELL="/bin/sh -c",
        )

"""
    Solaris command class containing system commands
    TODO -  Untested
"""
class SolarisCommands(BaseCommands):
    def __init__(self):
        super().__init__(
            NetStat="netstat -pan",
            PS="ps -eLf",
            PS2="ps -eLf",
            M3PS="ps -eLf",
            Disk="df -hk",
            #  TOCHECK - What is the TOP_INTERVAL is the frequency ? and what is script span
            # Top=f"top -bc -d {TOP_INTERVAL} -n {SCRIPT_SPAN//TOP_INTERVAL + 1}",
            # Top2=f"top -bc -d {TOP_INTERVAL} -n {SCRIPT_SPAN//TOP_INTERVAL + 1}",
            TopH="top -bH -n 1 -p {DynamicArg}",
            TopH2="top -bH -n 1 -p {DynamicArg}",
            Top4M3="top -bc -n 1",
            #  TOCHECK - What are the dynamic arguements
            #  VMState=f"vmstat {DynamicArg} {DynamicArg} | awk '{{now=strftime(\"%T \"); print now $0; fflush()}}'",
            DMesg="dmesg",
            DMesg2="dmesg",
            ProcessTopCPU="ps -eo pid,cmd,%cpu --sort=-%cpu",
            ProcessTopMEM="ps -eo pid,cmd,%mem --sort=-%mem",
            OSVersion="uname -a",
            KernelParam="sysctl -a",
            SHELL="/bin/sh -c"
        )
"""
    AIX command class containing system commands
    TODO -  Untested
"""
class AIXCommands(BaseCommands):
    def __init__(self):
        super().__init__(
            NetStat="netstat -a",
            PS="ps -ef",
            PS2="ps -ef",
            M3PS="ps -ef",
            Disk="df",
            Top="topas -P",
            Top2="topas -P",
            TopH="topas -P",
            TopH2="topas -P",
            Top4M3="topas -P",
            #  TOCHECK - What are dynamic arguments ?
            # VMState=Command("vmstat", DynamicArg, DynamicArg),
            DMesg="dmesg",
            DMesg2="dmesg",
            ProcessTopCPU="ps -eo pid,cmd,%cpu --sort=-%cpu",
            ProcessTopMEM="ps -eo pid,cmd,%mem --sort=-%mem",
            #  TOCHECK - What is WaitCommand why is it required
            # OSVersion=Command(WaitCommand, "uname", "-a"),
            # KernelParam=Command(WaitCommand, "sysctl", "-a"),
            SHELL="/bin/sh -c"
        )

"""
    Windoes command class containing system commands
    TODO -  Untested
"""
class WindowsCommands(BaseCommands):
    def __init__(self):
        super().__init__(
            NetStat="netstat -an",
            PS="PowerShell.exe -Command Get-CimInstance -Class Win32_Process | ConvertTo-Json",
            PS2="PowerShell.exe -Command Get-CimInstance -Class Win32_Process | ConvertTo-Json",
            M3PS="PowerShell.exe -Command Get-CimInstance -Class Win32_Process | ConvertTo-Json",
            Disk="wmic logicaldisk get size,freespace,caption",
            Top="NotSupported",
            Top2="NotSupported",  # Placeholder for no operation
            TopH="NotSupported",
            TopH2="NotSupported",  # Placeholder for no operation
            Top4M3="NotSupported",
            VMState= "PowerShell.exe -Command & {typeperf -sc 10 -si 5 \System\Processor Queue Length \PhysicalDisk(_Total)\Current Disk Queue Length \Process(_Total) \Page File Bytes \Memor \Available KBytes \Memory \Modified Page List Bytes \Memory \Cache Bytes \Memory \Pages Input/sec \Memory \Pages Output/sec \PhysicalDisk(_Total) \Disk Transfers/sec \PhysicalDisk(_Total) \Disk Writes/sec \Processor(_Total) \Interrupts/sec \System \Context Switches/sec \Processor(_Total) \% User Time \Processor(_Total) \% Privileged Time \Processor(_Total) \% Idle Time \Processor(_Total) \% Interrupt Time \Processor(_Total) \% DPC Time'}",
            DMesg="PowerShell.exe -Command & {Get-EventLog -LogName System -Newest 20 -EntryType Error,FailureAudit,Warning | Select-Object TimeGenerated, EntryType, Message | ForEach-Object { Write-Host $($_.TimeGenerated) [$($_.EntryType)]: $($_.Message) }}",
            DMesg2="wevtutil  qe System /c:20 /rd:true /f:text",
            ProcessTopCPU="PowerShell.exe -Command & {ps | sort -desc CPU}",
            ProcessTopMEM="PowerShell.exe -Command & {ps | sort -desc PM}",
            OSVersion="PowerShell.exe -Command & {systeminfo | findstr /B /C:OS Name /C:OS Version}",
            KernelParam="NotSupported",
            Ping=f"ping -c 6 {PING_ENDPOINT}",
            SHELL="cmd.exe /c"
                )


