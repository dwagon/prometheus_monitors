#!/usr/bin/env python3
""" Convert speedtest results to prometheus data """
# See https://www.speedtest.net/apps/cli

import json
import subprocess
from typing import Any

PROM_FILE="/var/lib/prometheus/node-exporter/speedtest.prom"

##############################################################################
def run_speedtest() -> dict[str, Any]:
    """ Run speedtest and return the json data """
    data = subprocess.run(["speedtest", "-f", "json"], capture_output=True, check=True)
    return json.loads(data.stdout)

##############################################################################
def save_result(outfh, helpstr: str, key: str, value:float, data_type="gauge"):
    outfh.write(f"# HELP {key} {helpstr}\n")
    outfh.write(f"# TYPE {key} {data_type}\n")
    outfh.write(f"{key} {int(value)}\n")

##############################################################################
def save_results(data: dict[str, Any]) -> None:
    with open(PROM_FILE, "w") as outfh:
        outfh.write(f"# {data['timestamp']}\n")
        save_result(outfh, "Packetloss", "packetloss", data["packetLoss"])
        save_result(outfh, "Upload IQM", "upload_iqm", data["upload"]["latency"]["iqm"])
        save_result(outfh, "Upload Speed Mbps", "upload_speed", data["upload"]["bandwidth"])
        save_result(outfh, "Download IQM", "download_iqm", data["download"]["bandwidth"])
        save_result(outfh, "Download Speed Mbps", "download_speed", data["upload"]["bandwidth"])
        save_result(outfh, "Ping latency", "ping_latency", data["ping"]["latency"])
        save_result(outfh, "Ping low", "ping_low", data["ping"]["low"])
        save_result(outfh, "Ping high", "ping_high", data["ping"]["high"])
        

##############################################################################
def main():
    data = run_speedtest()
    save_results(data)


##############################################################################
if __name__ == "__main__":
    main()

# EOF
