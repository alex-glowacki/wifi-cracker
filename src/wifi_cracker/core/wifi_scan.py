# src/wifi_cracker/core/wifi_scan.py

# Standard library
import platform
import subprocess
import re
from typing import List


def _run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="ignore")

def scan_ssids() -> List[str]:
    system = platform.system()
    
    if system == "Windows":
        out = _run(['netsh', "wlan", "show", "networks", "mode=bssid"])
        
        ssids = []
        
        for line in out.splitlines():
            m = re.match(r"\s*SSID\s+\d+\s*:\s*(.*)\s*$", line)
            if m:
                name = m.group(1).strip()
                if name and name.lower() != "<hidden>":
                    ssids.append(name)
        return sorted(set(ssids), key=str.lower)
    
    elif system == "Darwin":
        airport = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
        out = _run([airport, "-s"])
        
        ssids = []
        
        for line in out.splitlines()[1:]:
            line = line.rstrip()
            if not line:
                continue
            parts = re.split(r"\s{2,}", line)
            if parts:
                name = parts[0].strip()
                if name:
                    ssids.append(name)
        return sorted(set(ssids), key=str.lower)
    
    else:
        try:
            out = _run(["nmcli", "-t", "-f", "SSID", "dev", "wifi"])
            
            ssids = []
            
            for line in out.splitlines():
                name = line.strip()
                if name:
                    ssids.append(name)
            return sorted(set(ssids), key=str.lower)
        except Exception:
            out = _run(["iwlist", "scanning"])
            ssids = re.findall(r'ESSID:"(.*?)"', out)
            ssids = [s for s in ssids if s]
            return sorted(set(ssids), key=str.lower)