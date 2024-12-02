#!/usr/bin/env python3
""" Convert speedtest results to prometheus data """
# See https://www.speedtest.net/apps/cli

import json
import os
import subprocess
from typing import Any

PROM_DIR = os.environ.get("NODE_EXPORTER_DIR", "/var/lib/prometheus/node-exporter")
PROM_FILE = os.path.join(PROM_DIR, "speedtest.prom")


##############################################################################
def run_speedtest() -> dict[str, Any]:
    """Run speedtest and return the json data"""
    cmd = ["speedtest", "-f", "json"]
    data = subprocess.run(cmd, capture_output=True, check=True)
    return json.loads(data.stdout)


##############################################################################
def save_result(outfh, helpstr: str, key: str, value: float, data_type="gauge"):
    """Save a value to the {outfh} file"""
    key = f"speedtest_{key}"
    outfh.write(f"# HELP {key} {helpstr}\n")
    outfh.write(f"# TYPE {key} {data_type}\n")
    outfh.write(f"{key} {int(value)}\n")


##############################################################################
def save_results(data: dict[str, Any]) -> None:
    """Save all the results to a prom file"""
    with open(PROM_FILE, "w", encoding="utf-8") as outfh:
        outfh.write(f"# {data['timestamp']}\n")
        save_result(outfh, "Packetloss", "packetloss", data["packetLoss"])

        d = data["upload"]
        save_result(outfh, "Upload latency", "upload_latency", d["latency"]["iqm"])
        save_result(outfh, "Upload bandwidth bps", "upload_bandwidth", d["bandwidth"])
        save_result(outfh, "Upload bytes", "upload_bytes", d["bytes"])
        save_result(outfh, "Upload elapsed ms", "upload_elapsed", d["elapsed"])

        d = data["download"]
        save_result(outfh, "Download latency", "download_latency", d["latency"]["iqm"])
        save_result(outfh, "Download bandwidth bps", "download_bandwidth", d["bandwidth"])
        save_result(outfh, "Download bytes", "download_bytes", d["bytes"])
        save_result(outfh, "Download elapsed ms", "download_elapsed", d["elapsed"])

        d = data["ping"]
        save_result(outfh, "Ping latency", "ping_latency", d["latency"])
        save_result(outfh, "Ping low", "ping_low", d["low"])
        save_result(outfh, "Ping high", "ping_high", d["high"])


##############################################################################
def main():
    """Main"""
    data = run_speedtest()
    save_results(data)


##############################################################################
if __name__ == "__main__":
    main()

# EOF
