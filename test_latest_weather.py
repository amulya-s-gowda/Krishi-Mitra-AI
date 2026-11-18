
import requests
import pandas as pd
from datetime import date, timedelta

# Shivamogga district coordinates
latitude = 13.9299
longitude = 75.5681

today = date.today()
start_date = today - timedelta(days=14)

url = "https://power.larc.nasa.gov/api/temporal/daily/point"

parameters = {
    "parameters": "PRECTOTCORR,T2M,T2M_MAX,T2M_MIN,RH2M",
    "community": "AG",
    "longitude": longitude,
    "latitude": latitude,
    "start": start_date.strftime("%Y%m%d"),
    "end": today.strftime("%Y%m%d"),
    "format": "JSON"
}

response = requests.get(url, params=parameters, timeout=60)
response.raise_for_status()

weather_json = response.json()
weather_data = weather_json["properties"]["parameter"]

df = pd.DataFrame(weather_data)
df.index.name = "Date"
df = df.reset_index()

df["Date"] = pd.to_datetime(df["Date"], format="%Y%m%d")
df = df.replace(-999, pd.NA)

print("RECENT WEATHER DATA")
print("-------------------")
print(df.tail(7).to_string(index=False))

valid_data = df.dropna(
    subset=["PRECTOTCORR", "T2M", "T2M_MAX", "T2M_MIN", "RH2M"]
)

if not valid_data.empty:
    latest = valid_data.iloc[-1]
    print("\nLATEST VALID WEATHER RECORD")
    print("Date:", latest["Date"].date())
    print("Rainfall:", latest["PRECTOTCORR"], "mm")
    print("Temperature:", latest["T2M"], "°C")
    print("Maximum temperature:", latest["T2M_MAX"], "°C")
    print("Minimum temperature:", latest["T2M_MIN"], "°C")
    print("Humidity:", latest["RH2M"], "%")
else:
    print("\nNo valid weather records found.")
