import requests
from datetime import datetime, timedelta
from dateutil import parser
from database import get_client


def download_wind_measures(start, end, client):
    start = start.strftime("%Y-%m-%dT%H:%M:%S")
    end = end.strftime("%Y-%m-%dT%H:%M:%S")

    url = f"http://api.pioupiou.fr/v1/archive/23?start={start}&stop={end}&format=json"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        fields_names = [f"{colname}_{unit}" for colname,
                        unit in zip(data["legend"], data["units"])]
        fields = fields_names[1:len(fields_names) - 1]  # Remove time and preassure
        values = [measure[1:len(fields_names) - 1] for measure in data["data"]]
        times = [parser.parse(measure[0]).strftime("%Y-%m-%dT%H:%M:%SZ")
                for measure in data["data"]]

        influx_data = [{"fields": {fname: float(fvalue) for fname, fvalue in zip(
            fields, measure)}, "time": time, "tags": {}, "measurement": "v1"} for measure, time in zip(values, times)]

        client.write_points(influx_data)

