"""
   ___       ___      ___            __       
  / _ \__ __/ _ \___ / _/__ ___  ___/ /__ ____
 / ___/ // / // / -_) _/ -_) _ \/ _  / -_) __/
/_/   \_, /____/\__/_/ \__/_//_/\_,_/\__/_/   
     /___/                                    


Made with 💞 by kova / api
- Made with program protection in mind.
"""
import ctypes, os, sys, time, pkg_resources, socket, struct, requests, psutil, win32api
from typing import Literal
from ..types import Event, Logger
from ..abc import Module
from ..constants import UserInfo, Lists
from ..utils.http import hasInternet
from ..utils.webhook import Webhook

class Miscellaneous(Module):
    def __init__(self, webhook: Webhook, logger: Logger, exit: bool, report: bool, event: Event) -> None:
        self.webhook: Webhook = webhook
        self.logger: Logger = logger
        self.exit: bool = exit
        self.report: bool = report
        self.event: Event = event
    
    @property
    def name(self) -> str:
        return self.__class__.__name__
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    def CheckInternet(self) -> None:
        """
        Checks if the user has a valid interent connection or not

        Returns:
            Nothing
        """
        while True:
            time.sleep(5)
            if hasInternet() is False:
                if self.report:
                    self.logger.info("Check Internet Has Failed")
                if self.exit:
                    os._exit(1)

    def CheckRAM(self) -> None:
        """Checks RAM size, if less than 4gb, report."""
        memory: int = psutil.virtual_memory().total
        if memory <= 4294967296:
            self.logger.info("RAM Check Failed")
            if self.report:
                self.webhook.Send("Less than 4 GB of RAM exists on this system", self.name)
                self.event.dispatch(
                    "ram_check",
                    "Less than 4 GB of RAM exists on this system",
                    self.name,
                    ram=memory,
                )
                self.event.dispatch(
                    "pydefender_detect",
                    "Less than 4 GB of RAM exists on this system",
                    self.name,
                    ram=memory,
                )
            if self.exit:
                os._exit(1)


    def CheckIsDebuggerPresent(self) -> None:
        """Checks IsDebuggerPresent and CheckRemoteDebuggerPresent"""
        isDebuggerPresent = ctypes.windll.kernel32.IsDebuggerPresent()

        if isDebuggerPresent:
            self.logger.send("IsDebuggerPresent Returned True")
            if self.report:
                self.webhook.Send("IsDebuggerPresent Returned True", self.name)
                self.event.dispatch("is_debugger_present", "IsDebuggerPresent Returned True", self.name)
                self.event.dispatch("pydefender_detect", "IsDebuggerPresent Returned True", self.name
)
            if self.exit:
                os._exit(1)

        if (ctypes.windll.kernel32.CheckRemoteDebuggerPresent(
                ctypes.windll.kernel32.GetCurrentProcess(), False
            )!= 0
        ):
            self.logger.send("CheckRemoteDebuggerPresent Returned True")
            if self.report:
                self.webhook.Send("CheckRemoteDebuggerPresent returned `True`",self.name,)
                self.event.dispatch(
                    "check_remote_debugger_present",
                    "CheckRemoteDebuggerPresent Returned True",
                    self.name,
                )
                self.event.dispatch(
                    "pydefender_detect",
                    "CheckRemoteDebuggerPresent Returned True",
                    self.name,
                )
            if self.exit:
                os._exit(1)

    def CheckDiskSize(self) -> None:
        """Check Disk Size"""
        minDiskSizeGB: Literal[50] = 50
        if len(sys.argv) > 1:
            minDiskSizeGB = float(sys.argv[1])
        _, diskSizeBytes, _ = win32api.GetDiskFreeSpaceEx()
        diskSizeGB: int = diskSizeBytes / 1073741824

        if diskSizeGB < minDiskSizeGB:
            self.logger.info("Disk Check Failed")
            if self.report:
                self.webhook.Send(f"The current disk size is `{diskSizeGB}GB`, which is less than the minimum requirement.", self.name)
                self.event.dispatch(
                    "disk_size_check",
                    f"The Current Disk Size Is {diskSizeGB}GB, Which Is Less Than The Minimum",
                    self.name,
                    disk_size=diskSizeGB,
                )
                self.event.dispatch(
                    "pydefender_detect",
                    f"The Current Disk Size Is {diskSizeGB}GB, Which Is Less Than The Minimum",
                    self.name,
                    disk_size=diskSizeGB,
                )
            if self.exit:
                os._exit(1)

    def KillTasks(self) -> None:
        """Kills Common RE Tasks"""
        os.system("taskkill /f /im HTTPDebuggerUI.exe >nul 2>&1")
        os.system("taskkill /f /im HTTPDebuggerSvc.exe >nul 2>&1")
        os.system('taskkill /FI "IMAGENAME eq cheatengine*" /IM * /F /T >nul 2>&1')
        os.system('taskkill /FI "IMAGENAME eq httpdebugger*" /IM * /F /T >nul 2>&1')
        os.system('taskkill /FI "IMAGENAME eq processhacker*" /IM * /F /T >nul 2>&1')
        os.system('taskkill /FI "IMAGENAME eq fiddler*" /IM * /F /T >nul 2>&1')
        os.system('taskkill /FI "IMAGENAME eq wireshark*" /IM * /F /T >nul 2>&1')
        os.system('taskkill /FI "IMAGENAME eq rawshark*" /IM * /F /T >nul 2>&1')
        os.system('taskkill /FI "IMAGENAME eq charles*" /IM * /F /T >nul 2>&1')
        os.system('taskkill /FI "IMAGENAME eq cheatengine*" /IM * /F /T >nul 2>&1')
        os.system('taskkill /FI "IMAGENAME eq ida*" /IM * /F /T >nul 2>&1')
        os.system('taskkill /FI "IMAGENAME eq httpdebugger*" /IM * /F /T >nul 2>&1')
        os.system('taskkill /FI "IMAGENAME eq processhacker*" /IM * /F /T >nul 2>&1')
        os.system("sc stop HTTPDebuggerPro >nul 2>&1")
        os.system("sc stop KProcessHacker3 >nul 2>&1")
        os.system("sc stop KProcessHacker2 >nul 2>&1")
        os.system("sc stop KProcessHacker1 >nul 2>&1")
        os.system("sc stop wireshark >nul 2>&1")
        os.system("sc stop npf >nul 2>&1")
        os.system("sc stop HTTPDebuggerPro >nul 2>&1")
        os.system(
            'cmd.exe /c @RD /S /Q "C:\\Users\\%username%\\AppData\\Local\\Microsoft\\Windows\\INetCache\\IE" >nul 2>&1'
        )

    def CheckPaths(self) -> None:
        """Checks Paths on Computer Against Blacklisted Paths"""
        for path in Lists.BLACKLISTED_PATHS:
            if os.path.exists(path):
                self.logger.info("Blacklisted Path Found")
                if self.report:
                    self.webhook.Send("Blacklisted path found", self.name)
                    self.event.dispatch(
                        "blacklisted_path",
                        "Blacklisted Path Found",
                        module = self.name,
                        path=path,
                    )
                    self.event.dispatch(
                        "pydefender_detect",
                        "Blacklisted Path Found",
                        module = self.name,
                        path=path,
                    )
                if self.exit:
                    os._exit(1)
            else:
                pass

    def CheckImports(self) -> None:
        """Checks Current Installed PyPi Packages For Blacklisted Packages"""
        for package in Lists.BLACKLISTED_IMPORTS:
            try:
                dist = pkg_resources.get_distribution(package)
                if dist:
                    self.logger.info(f"{package} Was Found Installed")
                    if self.report:
                        self.webhook.Send(
                            f"`{package}` was found installed",
                            self.name,
                        )
                        self.event.dispatch(
                            "blacklisted_import",
                            f"{package} Was Found Installed",
                            self.name,
                            dist=dist,
                        )
                        self.event.dispatch(
                            "pydefender_detect",
                            f"{package} Was Found Installed",
                            self.name,
                            dist=dist,
                        )
                    if self.exit:
                        os._exit(1)
                else:
                    pass
            except pkg_resources.DistributionNotFound:
                pass

    def CheckOutPutDebugString(self) -> None:
        """Checks OutPutDebugString"""
        win32api.SetLastError(0)
        win32api.OutputDebugString("PythonProtector Intruding...")
        if win32api.GetLastError() != 0:
            self.logger.info("OutputDebugString Is Not 0")
            if self.report:
                self.webhook.Send("OutputDebugString Not Equal To 0", self.name)
                self.event.dispatch(
                    "output_debug_string", "OutputDebugString Not Equal To 0", self.name
                )
                self.event.dispatch(
                    "pydefender_detect", "OutputDebugString Not Equal To 0", self.name
                )
            if self.exit:
                os._exit(1)

    def CheckIPs(self) -> None:
        """Checks User IP Against Blacklisted List"""
        if UserInfo.IP in Lists.BLACKLISTED_IPS:
            self.logger.info(f"{UserInfo.IP} Is A Blacklisted IP Address")
            if self.report:
                self.webhook.Send(
                    f"`{UserInfo.IP}` is a blacklisted IP address", self.name
                )
                self.event.dispatch(
                    "ip_check",
                    f"{UserInfo.IP} Is A Blacklisted IP Address",
                    self.name,
                    ip=UserInfo.IP,
                )
                self.event.dispatch(
                    "pydefender_detect",
                    f"{UserInfo.IP} Is A Blacklisted IP Address",
                    self.name,
                    ip=UserInfo.IP,
                )
            if self.exit:
                os._exit(1)
        else:
            pass

    def CheckCPUCores(self) -> None:
        """Checks CPU Core Count For Being Less Than 1"""
        if int(psutil.cpu_count()) <= 1:
            self.logger.info("CPU Core Count Is Less Than Or Equal To 1")
            if self.report:
                self.webhook.Send("CPU core count is less than or equal to `1`", self.name)
                self.event.dispatch(
                    "cpu_count" "CPU Core Count Is Less Than Or Equal To 1", self.name
                )
                self.event.dispatch(
                    "pydefender_detect" "CPU Core Count Is Less Than Or Equal To 1",
                    self.name,
                )
            if self.exit:
                os._exit(1)

    def IsUsingProxy(self) -> None:
        """Checks If Proxies Are In Use"""
        headers: dict[str, str] = {"User-Agent": "Mozilla/5.0"}
        response = requests.get("https://www.google.com", headers=headers)
        for header in Lists.PROXY_HEADERS:
            if header in response.headers:
                self.logger.info("Proxy Headers In Use")
                if self.report:
                    self.webhook.Send("Proxy headers are in use", self.name)
                    self.event.dispatch(
                        "proxy_headers",
                        "Proxy Headers Being Used",
                        self.name,
                        header=header,
                    )
                    self.event.dispatch(
                        "pydefender_detect",
                        "Proxy Headers Being Used",
                        self.name,
                        header=header,
                    )
                if self.exit:
                    os._exit(1)

        if UserInfo.IP in Lists.PROXY_IPS:
            self.logger.info("Proxy IP In Use")
            if self.report:
                self.webhook.Send("Proxy IP being used", self.name)
                self.event.dispatch(
                    "proxy_ip", "Proxy IP Being Used", self.name, ip=UserInfo.IP
                )
                self.event.dispatch(
                    "pydefender_detect",
                    "Proxy IP Being Used",
                    self.name,
                    ip=UserInfo.IP,
                )
            if self.exit:
                os._exit(1)

        try:
            _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            _socket.settimeout(5)
            _socket.connect(("check.torproject.org", 9050))
            _socket.send(b"GET / HTTP/1.1\r\nHost: check.torproject.org\r\n\r\n")
            data: bytes = _socket.recv(1024)
            if "Congratulations" in data.decode():
                self.logger.info("Tor Network Detected")
                if self.report:
                    self.webhook.Send("Tor network in use", self.name)
                    self.event.dispatch("tor_network", "Tor Network In Use", self.name)
                    self.event.dispatch(
                        "pydefender_detect", "Tor Network In Use", self.name
                    )
                if self.exit:
                    os._exit(1)
        except Exception:
            pass

        try:
            IP = struct.unpack("!I", socket.inet_aton(UserInfo.IP))[0]
            if IP >> 24 in [0, 10, 100, 127, 169, 172, 192]:
                self.logger.info("Transparent Proxies Detected")
                if self.report:
                    self.webhook.Send("Transparent proxies detected", self.name)
                    self.event.dispatch(
                        "transparent_proxies", "Transparent Proxies Detected", self.name
                    )
                    self.event.dispatch(
                        "pydefender_detect", "Transparent Proxies Detected", self.name
                    )
                if self.exit:
                    os._exit(1)
        except Exception:
            pass

    def StartChecks(self) -> None:
        if self.report:
            self.logger.info("Starting Miscellaneous Checks")
        self.CheckImports()
        self.CheckPaths()
        self.CheckIPs()
        self.CheckCPUCores()
        self.CheckRAM()
        self.CheckIsDebuggerPresent()
        self.CheckOutPutDebugString()
        self.CheckDiskSize()
        self.KillTasks()
        self.IsUsingProxy()
        if self.report:
            self.logger.info("Finished Miscellaneous Checks")

        self.CheckInternet()