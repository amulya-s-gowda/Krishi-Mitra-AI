
import pandas as pd

# Load cleaned Karnataka weather dataset
df = pd.read_csv("data/karnataka_weather_cleaned.csv")

df["Date"] = pd.to_datetime(df["Date"])

# Assign farming season based on month
def get_season(month):

    if month in [6, 7, 8, 9, 10]:
        return "Kharif"

    elif month in [11, 12, 1, 2]:
        return "Rabi"

    else:
        return "Summer"


df["Month"] = df["Date"].dt.month
df["Season"] = df["Month"].apply(get_season)

# Calculate average climate for each district and season
climate_profiles = (
    df.groupby(["District", "Season"])
    [["PRECTOTCORR", "T2M", "RH2M"]]
    .mean()
    .reset_index()
)

climate_profiles = climate_profiles.round(2)

# Rename columns for easier use
climate_profiles = climate_profiles.rename(columns={
    "PRECTOTCORR": "Average_Rainfall",
    "T2M": "Average_Temperature",
    "RH2M": "Average_Humidity"
})

# Save the climate profiles
climate_profiles.to_csv(
    "data/district_season_climate.csv",
    index=False
)

print("\nDISTRICT SEASONAL CLIMATE PROFILES")
print("----------------------------------")

print(climate_profiles.head(15).to_string(index=False))

print("\nTotal district-season profiles:", len(climate_profiles))

print("\nSaved successfully: data/district_season_climate.csv")
