import requests
import pandas as pd
from pathlib import Path

district = "Shivamogga"
latitude = 13.9299
longitude = 75.5681

url = "https://power.larc.nasa.gov/api/temporal/daily/point"

params = {
    "parameters": "PRECTOTCORR,T2M,T2M_MAX,T2M_MIN,RH2M",
    "community": "AG",
    "longitude": longitude,
    "latitude": latitude,
    "start": "20130101",
    "end": "20251231",
    "format": "JSON"
}

print("Requesting NASA POWER historical data for", district)

response = requests.get(url, params=params, timeout=180)
response.raise_for_status()

result = response.json()
weather = result["properties"]["parameter"]

df = pd.DataFrame(weather)
df.index.name = "Date"
df = df.reset_index()

df["Date"] = pd.to_datetime(df["Date"], format="%Y%m%d")
df["District"] = district

for column in ["PRECTOTCORR", "T2M", "T2M_MAX", "T2M_MIN", "RH2M"]:
    df[column] = pd.to_numeric(df[column], errors="coerce")
    df[column] = df[column].replace(-999, float("nan"))

output = Path("data/historical_2013_2025_test")
output.mkdir(parents=True, exist_ok=True)

file_path = output / "shivamogga_test.csv"
df.to_csv(file_path, index=False)

print("\nNASA POWER test completed!")
print("Total records:", len(df))
print("First date:", df["Date"].min().date())
print("Last date:", df["Date"].max().date())
print("\nMissing values:")
print(df.isna().sum())
print("\nFirst five records:")
print(df.head().to_string(index=False))
print("\nSaved to:", file_path)
