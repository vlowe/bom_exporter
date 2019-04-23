from datetime import datetime, timezone
import time
import requests

from prometheus_client import start_http_server, Summary
from prometheus_client.core import GaugeMetricFamily, REGISTRY, GaugeMetricFamily

urls = [
    "http://www.bom.gov.au/fwo/IDN60801/IDN60801.94767.json",
    "http://www.bom.gov.au/fwo/IDN60901/IDN60901.94768.json",
]


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

        bom_pressure = GaugeMetricFamily(
            name="bom_pressure",
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

        for url in urls:
            data = requests.get(url).json()

            latest_obs = data["observations"]["data"][0]

            unix_epoch = (
                datetime.strptime(latest_obs["aifstime_utc"], "%Y%m%d%H%M%f")
                .replace(tzinfo=timezone.utc)
                .timestamp()
            )

            bom_utctimestamp.add_metric([latest_obs["name"]], unix_epoch)
            bom_air_temperature.add_metric([latest_obs["name"]], latest_obs["air_temp"])
            bom_pressure.add_metric([latest_obs["name"]], latest_obs["press"])
            bom_relative_humidity.add_metric(
                [latest_obs["name"]], latest_obs["rel_hum"]
            )
            bom_wind_speed.add_metric([latest_obs["name"]], latest_obs["wind_spd_kmh"])

        yield bom_utctimestamp
        yield bom_air_temperature
        yield bom_pressure
        yield bom_relative_humidity
        yield bom_wind_speed


# Query the BOM
REGISTRY.register(BOMCollector())
start_http_server(8000)

while True:
    time.sleep(60)
