
import requests
from datetime import datetime, timedelta
from dateutil import parser


now = datetime.today() - timedelta(hours=1)
last_hour = now - timedelta(hours=2)



def download_weather_measures(start, end, client, api_key):
    start = start.strftime("%Y-%m-%d")
    end = end.strftime("%Y-%m-%d")

    command = "https://api.meteostat.net/v2/stations/nearby?lat=44.9074&lon=5.6711&radius=60"
    headers = {"x-api-key": api_key}
    response = requests.get(command, headers=headers)
    data_header = {
        "temp": "temperature_celsius",
        "dwpt": "dew_point_celsius",
        "rhum": "relative_humidity_percent",
        "pres": "preassure_hpa",
        "coco": "condition_code",
    }
    if response.status_code == 200:
        stations = response.json()["data"]
        for station in stations:
            command_temp = f'https://api.meteostat.net/v2/stations/hourly?station={station["id"]}&start={start}&end={end}'
            response_temp = requests.get(command_temp, headers=headers)
            if response_temp.status_code == 200 and response_temp.json()["data"] is not None:
                influx_data = []
                for measure in response_temp.json()["data"]:
                    if measure["temp"] is not None:

                        time = parser.parse(measure["time"])
                        measure_data = {data_header[k]: float(v) for k,
                                        v in measure.items() if v is not None and k != "time"}
                        point = {
                            "fields": measure_data,
                            "tags": {},
                            "time": time,
                            "measurement": "v1"
                        }
                        influx_data.append(point)

        client.write_points(influx_data)
