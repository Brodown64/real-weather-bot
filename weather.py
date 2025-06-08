import openmeteo_requests


import pandas as pd #creates dataframe from hourly data
import requests_cache
from retry_requests import retry

from main import num1, num2

cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 44.7677, # change these two to smth editable (num1 and num2)
	"longitude": -93.2777,
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

# minutely 15 data
minutely_15 = response.Minutely15()
minutely_15_precision = minutely_15.Variables(0).ValuesAsNumpy()

minutely_15_data = {"date": pd.date_range(
	start = pd.to_datetime(minutely_15.Time(), unit = "s", utc = True),
	end = pd.to_datetime(minutely_15.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = minutely_15.Interval()),
	inclusive = "left"
	)}

minutely_15_data["precipitation"] = minutely_15_precision

minutely_15_dataframe = pd.DataFrame(data = minutely_15_data)
print(minutely_15_dataframe)

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_weather_code = hourly.Variables(1).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}

hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["weather_code"] = hourly_weather_code

hourly_dataframe = pd.DataFrame(data = hourly_data)
print(hourly_dataframe)

# look at weather code