
import pandas as pd
import numpy as np

# Load cleaned weather dataset
df = pd.read_csv("data/karnataka_weather_cleaned.csv")

# Convert date column
df["Date"] = pd.to_datetime(df["Date"])

# Sort records district-wise and date-wise
df = df.sort_values(
    by=["District", "Date"]
).reset_index(drop=True)

# Create next-day rainfall target
df["Next_Day_Rainfall"] = (
    df.groupby("District")["PRECTOTCORR"].shift(-1)
)

# Previous rainfall information
df["Rainfall_Lag_1"] = (
    df.groupby("District")["PRECTOTCORR"].shift(1)
)

df["Rainfall_Lag_2"] = (
    df.groupby("District")["PRECTOTCORR"].shift(2)
)

df["Rainfall_Lag_3"] = (
    df.groupby("District")["PRECTOTCORR"].shift(3)
)

# Average rainfall over the previous 3 days
df["Rainfall_3_Day_Avg"] = (
    df.groupby("District")["PRECTOTCORR"]
    .transform(lambda x: x.shift(1).rolling(3).mean())
)

# Extract month
df["Month"] = df["Date"].dt.month

# Represent seasonal date patterns
day_of_year = df["Date"].dt.day_of_year

df["Day_Sin"] = np.sin(2 * np.pi * day_of_year / 365.25)
df["Day_Cos"] = np.cos(2 * np.pi * day_of_year / 365.25)

# Remove records without enough historical information
df = df.dropna()

# Save prepared dataset
df.to_csv("data/weather_prediction_dataset.csv", index=False)

# Display results
print("ML DATASET PREPARED SUCCESSFULLY!")
print("----------------------------------")

print("Total records:", len(df))
print("Total districts:", df["District"].nunique())

print("\nAvailable columns:")
print(df.columns.tolist())

print("\nFirst five records:")
print(df.head())

print("\nSaved as: data/weather_prediction_dataset.csv")
