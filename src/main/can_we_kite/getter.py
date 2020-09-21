from weather import download_weather_measures
from wind import download_wind_measures
from webcam import take_screenshot
from datetime import datetime, timedelta
from database import get_client
import json

with open("configuration.json", "r", encoding="utf-8") as handler:
    configuration = json.loads(handler.read())

def get_date_yesterday():
    yesterday = datetime.today().date() - timedelta(days=1)
    return yesterday


yesterday = get_date_yesterday()
client = get_client()

download_wind_measures(start=yesterday, end=yesterday +
                       timedelta(days=1), client=client)
download_weather_measures(start=yesterday, end=yesterday+timedelta(days=1),
                          client=client, api_key=configuration["weather_api_key"])
take_screenshot(date=datetime.today())
client.close()
