```python
#!/usr/bin/env python3

import os
import platform
import shutil
import socket
from datetime import datetime

def get_memory_usage():
    try:
        with open("/proc/meminfo", "r") as file:
            meminfo = {}

            for line in file:
                parts = line.split()
                meminfo[parts[0].rstrip(":")] = int(parts[1])

        total = meminfo["MemTotal"]
        available = meminfo["MemAvailable"]
        used = total - available

        return (
            total / 1024,
            used / 1024,
            (used / total) * 100
        )
    except (OSError, KeyError, ValueError):
        return None, None, None


def get_disk_usage():
    usage = shutil.disk_usage("/")
    total = usage.total / (1024 ** 3)
    used = usage.used / (1024 ** 3)
    percent = (usage.used / usage.total) * 100

    return total, used, percent


def generate_report():
    hostname = socket.gethostname()
    os_name = platform.system()
    os_release = platform.release()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    memory_total, memory_used, memory_percent = get_memory_usage()
    disk_total, disk_used, disk_percent = get_disk_usage()
    load_avg = os.getloadavg() if hasattr(os, "getloadavg") else None

    report = f"""
========================================
       EC2 SYSTEM HEALTH REPORT
========================================

Generated At : {current_time}
Hostname     : {hostname}
Operating OS : {os_name}
Kernel       : {os_release}

--------------- MEMORY -----------------
Total Memory : {memory_total:.2f} MB
Used Memory  : {memory_used:.2f} MB
Memory Usage : {memory_percent:.2f}%

---------------- DISK ------------------
Total Disk   : {disk_total:.2f} GB
Used Disk    : {disk_used:.2f} GB
Disk Usage   : {disk_percent:.2f}%

--------------- CPU LOAD ---------------
"""

    if load_avg:
        report += (
            f"1-minute Load  : {load_avg[0]:.2f}\n"
            f"5-minute Load : {load_avg[1]:.2f}\n"
            f"15-minute Load: {load_avg[2]:.2f}\n"
        )
    else:
        report += "CPU load information unavailable\n"

    report += "\n========================================\n"

    print(report)

    # Save report to a local file
    report_dir = os.path.expanduser("~/system-health-reports")
    os.makedirs(report_dir, exist_ok=True)

    filename = datetime.now().strftime("health_report_%Y%m%d_%H%M%S.txt")
    filepath = os.path.join(report_dir, filename)

    with open(filepath, "w") as file:
        file.write(report)

    print(f"Report saved at: {filepath}")


if __name__ == "__main__":
    generate_report()
```
