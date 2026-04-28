#!/usr/bin/env python3
""" Check if any downloads have arrived """

import os
from typing import Any

PROM_DIR = os.environ.get("NODE_EXPORTER_DIR", "/var/lib/prometheus/node-exporter")
PROM_FILE = os.path.join(PROM_DIR, "downloads.prom")


##############################################################################
def check_dir() -> int:
    """Number of entries"""
    files = os.listdir("/downloads/complete")
    return len(files)


##############################################################################
def save_result(outfh, helpstr: str, key: str, value: float, data_type="gauge"):
    """Save a value to the {outfh} file"""
    key = f"speedtest_{key}"
    outfh.write(f"# HELP {key} {helpstr}\n")
    outfh.write(f"# TYPE {key} {data_type}\n")
    outfh.write(f"{key} {value}\n")


##############################################################################
def save_results(num: int) -> None:
    """Save all the results to a prom file"""
    with open(PROM_FILE, "w", encoding="utf-8") as outfh:
        save_result(outfh, "Number downloads", "num_downloads", num)


##############################################################################
def main():
    """Main"""
    data = check_dir()
    save_results(data)


##############################################################################
if __name__ == "__main__":
    main()

# EOF
