
import pandas as pd

# Load historical daily weather data
df = pd.read_csv("data/karnataka_weather_cleaned.csv")

df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month

# Define farming seasons
def get_season(month):
    if month in [6, 7, 8, 9, 10]:
        return "Kharif"
    elif month in [11, 12, 1, 2]:
        return "Rabi"
    else:
        return "Summer"

df["Season"] = df["Month"].apply(get_season)

# Remove missing rainfall records
df = df.dropna(subset=["PRECTOTCORR"])

# Calculate rainfall totals by district, year and season
seasonal_rainfall = (
    df.groupby(["District", "Year", "Season"])["PRECTOTCORR"]
    .sum()
    .reset_index()
)

print("\nSEASONAL RAINFALL TOTALS")
print("------------------------")

# Show Shivamogga as an example
shivamogga = seasonal_rainfall[
    seasonal_rainfall["District"] == "Shivamogga"
]

print(shivamogga.to_string(index=False))

# Calculate average seasonal rainfall across years
average_rainfall = (
    seasonal_rainfall.groupby(["District", "Season"])
    ["PRECTOTCORR"]
    .mean()
    .reset_index()
)

average_rainfall.rename(
    columns={"PRECTOTCORR": "Average_Seasonal_Rainfall_mm"},
    inplace=True
)

average_rainfall["Average_Seasonal_Rainfall_mm"] = (
    average_rainfall["Average_Seasonal_Rainfall_mm"].round(2)
)

average_rainfall.to_csv(
    "data/district_seasonal_rainfall_totals.csv",
    index=False
)

print("\nAVERAGE SEASONAL RAINFALL - SHIVAMOGGA")
print("--------------------------------------")

print(
    average_rainfall[
        average_rainfall["District"] == "Shivamogga"
    ].to_string(index=False)
)

print("\nTotal district-season records:", len(average_rainfall))

print("\nSaved: data/district_seasonal_rainfall_totals.csv")
