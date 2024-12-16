#!/usr/bin/python3
""" Get weather data from weatherapi.com """


import json
import os
import sys
import urllib.request
from typing import Any


PROM_DIR = os.environ.get("NODE_EXPORTER_DIR", "/var/lib/prometheus/node-exporter")
PROM_FILE = os.path.join(PROM_DIR, "weather.prom")


##############################################################################
def get_url() -> str:
    """ Construct the API URL """
    try:
        weather_api_key = os.environ["WEATHER_API_KEY"]
    except KeyError:
        print("Need to specify WEATHER_API_KEY", file=sys.stderr)
        sys.exit(1)
    try:
        weather_location = os.environ["WEATHER_LOCATION"]
    except KeyError:
        print("Need to specify WEATHER_LOCATION", file=sys.stderr)
        sys.exit(1)

    url = f"https://api.weatherapi.com/v1/current.json"
    url += f"?key={weather_api_key}"
    url += f"&q={weather_location}"
    url += "&aqi=yes"
    return url


##############################################################################
def get_data(url: str) -> dict[str, Any]:
    """ Get the data from the website """

    with urllib.request.urlopen(url) as infh:
        data = infh.read().decode('utf-8')
    return json.loads(data)


##############################################################################
def save_result(outfh, helpstr: str, key: str, value: float, data_type="gauge"):
    """Save a value to the {outfh} file"""
    key = f"weather_{key}"
    outfh.write(f"# HELP {key} {helpstr}\n")
    outfh.write(f"# TYPE {key} {data_type}\n")
    outfh.write(f"{key} {value}\n")


##############################################################################
def save_results(data: dict[str, Any]):
    """ Save the results in a prom file """
    current = data["current"]
    aqi = data["current"]["air_quality"]
    with open(PROM_FILE, "w", encoding="utf-8") as outfh:
        outfh.write(f"# Collected from API {data['location']['localtime']}\n")
        outfh.write(f"# Data from {current['last_updated']}\n")
        save_result(outfh, "Current Temp in degrees c", "temp", current['temp_c'])
        save_result(outfh, "Wind Speed kph", "wind_speed", current['wind_kph'])
        save_result(outfh, "Gust Speed kph", "gust_speed", current['gust_kph'])
        save_result(outfh, "Wind Direction", "wind_dir", current['wind_degree'])
        save_result(outfh, "Precipitation mm", "precip", current['precip_mm'])
        save_result(outfh, "UV", "uv", current['uv'])
        save_result(outfh, "Humidity", "humidity", current['humidity'])
        save_result(outfh, "Carbon Monoxide ug/m3", "aqi_co", aqi['co'])
        save_result(outfh, "Nitrogen Dioxide ug/m3", "aqi_no", aqi['no2'])
        save_result(outfh, "Ozon ug/m3", "aqi_o3", aqi['o3'])
        save_result(outfh, "Sulfur Dioxide ug/m3", "aqi_so2", aqi['so2'])
        save_result(outfh, "PM 2.5ug/m3", "aqi_pm2_5", aqi['pm2_5'])
        save_result(outfh, "PM 10 ug/m3", "aqi_pm10", aqi['pm10'])
        save_result(outfh, "US EPA Index", "aqi_epa", aqi['us-epa-index'])


##############################################################################
def main():
    """ Main """
    url = get_url()
    data = get_data(url)
    save_results(data)

##############################################################################
if __name__ == "__main__":
    main()

# EOF
