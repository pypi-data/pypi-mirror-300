"""
   ___       ___      ___            __       
  / _ \__ __/ _ \___ / _/__ ___  ___/ /__ ____
 / ___/ // / // / -_) _/ -_) _ \/ _  / -_) __/
/_/   \_, /____/\__/_/ \__/_//_/\_,_/\__/_/   
     /___/                                    


Made with 💞 by kova / api
- Made with program protection in mind.
"""
import os, re, wmi, subprocess, uuid
from typing import Final, List, Set, Any, final
from cryptography.fernet import Fernet
from base64 import b64encode
from .utils.http import getIpAddress
from . import __version__

@final
class UserInfo:
    USERNAME: Final[str] = os.getlogin()
    PC_NAME: Final[str] = os.getenv("COMPUTERNAME")
    IP: Final[str] = getIpAddress()
    HWID: Final[str] = (subprocess.check_output("wmic csproduct get uuid").decode().split("\n")[1].strip())
    COMPUTER: Any = wmi.WMI()
    MAC: Final[str] = ":".join(re.findall("..", "%012x" % uuid.getnode()))
    GPU: Final[str] = COMPUTER.Win32_VideoController()[0].Name

@final
class LoggingInfo:
    KEY: bytes = Fernet.generate_key()
    CIPHER: Fernet = Fernet(KEY)

    def encrypted_formatter(record) -> str:
        encrypted: bytes = LoggingInfo.CIPHER.encrypt(record["message"].encode("utf8"))
        record["extra"]["encrypted"] = b64encode(encrypted).decode("latin1")
        return "[{time:YYYY-MM-DD HH:mm:ss}] {module}::{function}({line}) - {extra[encrypted]}\n{exception}"

@final
class DefenderInfo:
    VERSION: Final[str] = __version__
    ROOT_PATH: str = os.path.abspath(os.curdir)

@final
class EmbedCfg:
    COLOR: Final[str] = "564BDC"
    TITLE: Final[str] = f"PyDefender - V{DefenderInfo.VERSION}"
    VERSION: Final[str] = DefenderInfo.VERSION
    ICON: Final[str] = "https://ripkova.github.io/cdn/PyDefender.png"

@final
class Lists:
    """
    To format the list (make it readable) use something like:
        - https://codebeautify.org/python-formatter-beautifier
        - https://www.tutorialspoint.com/online_python_formatter.htm
    """
    BLACKLISTED_PROGRAMS: Final[List[str]] = ['httpdebuggerui.exe','wireshark.exe','HTTPDebuggerSvc.exe','fiddler.exe','regedit.exe','taskmgr.exe','vboxservice.exe','df5serv.exe','processhacker.exe','vboxtray.exe','vmtoolsd.exe','vmwaretray.exe','ida.exe','ida64.exe','ollydbg.exe','pestudio.exe','vmwareuser','vgauthservice.exe','vmacthlp.exe','x96dbg.exe','vmsrvc.exe','x32dbg.exe','vmusrvc.exe','prl_cc.exe','prl_tools.exe','xenservice.exe','qemu-ga.exe','joeboxcontrol.exe','ksdumperclient.exe','ksdumper.exe','joeboxserver.exe']
    BLACKLISTED_DLLS: Final[List[str]] = ["sbiedll.dll","api_log.dll","dir_watch.dll","pstorec.dll","vmcheck.dll","wpespy.dll","crack.dll","cheat.dll","bypass.dll",]
    VIRTUAL_MACHINE_PROCESSES: Final[List[str]] = ["xenservice.exe","VMSrvc.exe","VMUSrvc.exe","VMwareService.exe","VMwareTray.exe","vboxservice.exe","vboxtray.exe","qemu-ga.exe","vdagent.exe","vdservice.exe",]
    BLACKLISTED_WINDOW_NAMES: Final[List[str]] = ['IDA: Quick start','VBoxTrayToolWndClass','VBoxTrayToolWnd','proxifier','graywolf','extremedumper','zed','exeinfope','titanHide','ilspy','titanhide','x32dbg','codecracker','simpleassembly','process hacker 2','pc-ret','http debugger','Centos','process monitor','debug','ILSpy','reverse','simpleassemblyexplorer','process','de4dotmodded','dojandqwklndoqwd-x86','sharpod','folderchangesview','fiddler','die','pizza','crack','strongod','ida -','brute','dump','StringDecryptor','wireshark','debugger','httpdebugger','gdb','kdb','x64_dbg','windbg','x64netdumper','petools','scyllahide','megadumper','reversal','ksdumper v1.1 - by equifox','dbgclr','HxD','monitor','peek','ollydbg','ksdumper','http','wpe pro','dbg','httpanalyzer','httpdebug','PhantOm','kgdb','james','x32_dbg','proxy','phantom','mdbg','WPE PRO','system explorer','de4dot','x64dbg','X64NetDumper','protection_id','charles','systemexplorer','pepper','hxd','procmon64','MegaDumper','ghidra','xd','0harmony','dojandqwklndoqwd','hacker','process hacker','SAE','mdb','checker','harmony','Protection_ID','PETools','scyllaHide','x96dbg','systemexplorerservice','folder','mitmproxy','dbx','sniffer','http toolkit']
    BLACKLISTED_PATHS: Final[List[str]] = [r"D:\Tools", r"D:\OS2", r"D:\NT3X"]
    BLACKLISTED_IPS: Final[list[str]] = ['None','88.132.231.71','78.139.8.50','20.99.160.173','88.153.199.169','84.147.62.12','194.154.78.160','92.211.109.160','195.74.76.222','188.105.91.116','34.105.183.68','92.211.55.199','79.104.209.33','95.25.204.90','34.145.89.174','109.74.154.90','109.145.173.169','34.141.146.114','212.119.227.151','195.239.51.59','192.40.57.234','64.124.12.162','34.142.74.220','188.105.91.173','34.105.72.241','109.74.154.92','213.33.142.50','93.216.75.209','192.87.28.103','88.132.226.203','195.181.175.105','88.132.225.100','92.211.192.144','34.83.46.130','188.105.91.143','34.85.243.241','34.141.245.25','178.239.165.70','84.147.54.113','193.128.114.45','95.25.81.24','92.211.52.62','88.132.227.238','35.199.6.13','80.211.0.97','34.85.253.170','23.128.248.46','35.229.69.227','34.138.96.23','192.211.110.74','35.237.47.12','87.166.50.213','34.253.248.228','212.119.227.167','193.225.193.201','34.145.195.58','34.105.0.27','195.239.51.3','35.192.93.107','213.33.190.22','194.154.78.152']
    BLACKLISTED_IMPORTS: Final[List[str]] = ["pydecipher","unpy2exe","uncompyle6","pefile","marshal","unpy2exe","pyarmor","pyarmor-webui","pyinject",]
    PROXY_IPS: Final[List[str]] = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]
    PROXY_HEADERS: Final[List[str]] = ["Via", "Forwarded", "X-Forwarded-For"]

@final
class Valid:
    Modules: Final[Set[str]] = {
        "Miscellaneous",
        "AntiProcess",
        "AntiDLL",
        "AntiVM",
        "AntiAnalysis",
        "AntiDump",
    }
    Detections: Final[Set[str]] = {"Screenshot", "Exit", "Report"}
