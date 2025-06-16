import openmeteo_requests


import pandas as pd #creates dataframe from hourly data
import requests
import requests_cache
from retry_requests import retry

# from main import num1, num2

cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 35.6764, # change these two to smth editable (num1 and num2)
    "longitude": -139.65,
    "hourly": ["temperature_2m", "weather_code"],
    "models": "gfs_global",
    "current": "temperature_2m",
    "timezone": "America/Chicago",
    "minutely_15": "precipitation",
    "temperature_unit": "fahrenheit",

}

responses = openmeteo.weather_api(url, params=params)

# first location
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()}{response.UtcOffsetSeconds()} s")

# current values
current = response.Current()
current_temperature_2m = current.Variables(0).Value()

print(f"Current time {current.Time()}")
print(f"Current_temperature_2m {current_temperature_2m}")
