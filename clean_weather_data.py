
import pandas as pd
from pathlib import Path

# Load the master dataset
file_path = Path("data/karnataka_master_weather.csv")
df = pd.read_csv(file_path)

print("Original dataset shape:", df.shape)

# Convert Date into datetime format
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Convert weather columns into numeric values
weather_columns = [
    "PRECTOTCORR",
    "T2M",
    "T2M_MAX",
    "T2M_MIN",
    "RH2M"
]

for column in weather_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Replace invalid NASA POWER values
df[weather_columns] = df[weather_columns].replace(-999, pd.NA)

# Remove duplicate district-date records
df = df.drop_duplicates(subset=["District", "Date"])

# Remove records with missing district or date
df = df.dropna(subset=["District", "Date"])

# Check invalid weather values
df.loc[df["PRECTOTCORR"] < 0, "PRECTOTCORR"] = pd.NA
df.loc[(df["RH2M"] < 0) | (df["RH2M"] > 100), "RH2M"] = pd.NA
df.loc[(df["T2M_MAX"] < df["T2M_MIN"]), ["T2M_MAX", "T2M_MIN"]] = pd.NA

# Display missing values before handling them
print("\nMissing values:")
print(df[weather_columns].isnull().sum())

# Save cleaned dataset
output_path = Path("data/karnataka_weather_cleaned.csv")
df.to_csv(output_path, index=False)

print("\nCleaned dataset shape:", df.shape)
print("Cleaned data saved successfully!")
print("File:", output_path)
