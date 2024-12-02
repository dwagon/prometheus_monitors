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

        d = data["upload"]
        save_result(outfh, "Upload latency", "speedtest_upload_latency", d["latency"]["iqm"])
        save_result(outfh, "Upload bandwidth bps", "speedtest_upload_bandwidth", d["bandwidth"])
        save_result(outfh, "Upload bytes", "speedtest_upload_bytes", d["bytes"])
        save_result(outfh, "Upload elapsed ms", "speedtest_upload_elapsed", d["elapsed"])

        d = data["download"]
        save_result(outfh, "Download latency", "speedtest_download_latency", d["latency"]["iqm"])
        save_result(outfh, "Download bandwidth bps", "speedtest_download_bandwidth", d["bandwidth"])
        save_result(outfh, "Download bytes", "speedtest_download_bytes", d["bytes"])
        save_result(outfh, "Download elapsed ms", "speedtest_download_elapsed", d["elapsed"])

        d = data["ping"]
        save_result(outfh, "Ping latency", "speedtest_ping_latency", d["latency"])
        save_result(outfh, "Ping low", "speedtest_ping_low", d["low"])
        save_result(outfh, "Ping high", "speedtest_ping_high", d["high"])
        

##############################################################################
def main():
    data = run_speedtest()
    save_results(data)


##############################################################################
if __name__ == "__main__":
    main()

# EOF
