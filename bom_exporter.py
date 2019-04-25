from datetime import datetime, timezone
import time
import requests

from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

urls = [
    "http://www.bom.gov.au/fwo/IDN60801/IDN60801.94767.json",
    "http://www.bom.gov.au/fwo/IDN60901/IDN60901.94768.json",
]

WIND_DIR_TO_TURN_FRACTIONS = {
    "N":    0/16,
    "NNE":  1/16,
    "NE":   2/16,
    "NEE":  3/16,
    "E":    4/16,
    "SEE":  5/16,
    "SE":   6/16,
    "SSE":  7/16,
    "S":    8/16,
    "SSW":  9/16,
    "SW":  10/16,
    "SWW": 11/16,
    "W":   12/16,
    "WNW": 13/16,
    "NW":  14/16,
    "NNW": 15/16,
}

WIND_DIR_TO_DEGREES = {dir: fraction*360 for dir,
                       fraction in WIND_DIR_TO_TURN_FRACTIONS.items()}


session = requests.Session()

class BOMCollector:
    def collect(self):
        bom_utctimestamp = GaugeMetricFamily(
            "bom_utctimestamp",
            documentation="UTC timestamp from the Bureau of Meterology (in Unix epoch)",
            labels=["location"],
        )

        bom_air_temperature = GaugeMetricFamily(
            name="bom_air_temperature",
            documentation="Air temperature from the Bureau of Meterology",
            labels=["location"],
        )

        bom_pressure_pascals = GaugeMetricFamily(
            name="bom_pressure_pascals",
            documentation="Pressure from the Bureau of Meterology",
            labels=["location"],
        )

        bom_relative_humidity = GaugeMetricFamily(
            name="bom_relative_humidity",
            documentation="Relative humidity from the Bureau of Meterology",
            labels=["location"],
        )

        bom_wind_speed = GaugeMetricFamily(
            name="bom_wind_speed",
            documentation="Wind speed (km/h) from the Bureau of Meterology",
            labels=["location"],
        )

        bom_wind_direction_degrees = GaugeMetricFamily(
            name="bom_wind_direction_degrees",
            documentation="Wind direction (degrees from true North) from the Bureau of Meterology",
            labels=["location"],
        )

        bom_apparent_temperature_celsius = GaugeMetricFamily(
            name="bom_apparent_temperature_celsius",
            documentation="Temperature, taking into account wind+humidity, from the Bureau of Meterology",
            labels=["location"],
        )

        for url in urls:
            data = session.get(url).json()

            latest_obs = data["observations"]["data"][0]

            unix_epoch = (
                datetime.strptime(latest_obs["aifstime_utc"], "%Y%m%d%H%M%f")
                .replace(tzinfo=timezone.utc)
                .timestamp()
            )

            labels = [latest_obs["name"]]
            bom_utctimestamp.add_metric(labels, unix_epoch)
            bom_air_temperature.add_metric(labels, latest_obs["air_temp"])
            bom_pressure_pascals.add_metric(
                labels, latest_obs["press"]*100)  # hPa to Pa
            bom_relative_humidity.add_metric(labels, latest_obs["rel_hum"])
            bom_wind_speed.add_metric(labels, latest_obs["wind_spd_kmh"])
            bom_apparent_temperature_celsius.add_metric(
                labels, latest_obs["apparent_t"])

            wind_dir = latest_obs["wind_dir"]
            if wind_dir in WIND_DIR_TO_DEGREES:
                bom_wind_direction_degrees.add_metric(
                    labels, WIND_DIR_TO_DEGREES[wind_dir])

        yield bom_utctimestamp
        yield bom_air_temperature
        yield bom_pressure_pascals
        yield bom_relative_humidity
        yield bom_wind_speed
        yield bom_wind_direction_degrees
        yield bom_apparent_temperature_celsius


# Query the BOM
REGISTRY.register(BOMCollector())
start_http_server(8000)

while True:
    time.sleep(60)
