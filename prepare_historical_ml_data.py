
import pandas as pd
import numpy as np
from pathlib import Path

# -----------------------------------------
# 1. LOAD HISTORICAL WEATHER DATA
# -----------------------------------------

INPUT_FILE = "data/karnataka_weather_2013_2025.csv"
OUTPUT_FILE = "data/historical_weather_prediction_dataset.csv"

df = pd.read_csv(INPUT_FILE)

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values(
    ["District", "Date"]
).reset_index(drop=True)

print("Original records:", len(df))


# -----------------------------------------
# 2. CREATE NEXT-DAY RAINFALL TARGET
# -----------------------------------------

df["Next_Day_Rainfall"] = (
    df.groupby("District")["PRECTOTCORR"].shift(-1)
)


# -----------------------------------------
# 3. CREATE RAINFALL LAG FEATURES
# -----------------------------------------

district_rainfall = df.groupby("District")["PRECTOTCORR"]

df["Rainfall_Lag_1"] = district_rainfall.shift(1)

df["Rainfall_Lag_2"] = district_rainfall.shift(2)

df["Rainfall_Lag_3"] = district_rainfall.shift(3)


# -----------------------------------------
# 4. CREATE 3-DAY RAINFALL AVERAGE
# -----------------------------------------

df["Rainfall_3_Day_Avg"] = (
    df.groupby("District")["PRECTOTCORR"]
    .transform(
        lambda series:
        series.shift(1).rolling(window=3).mean()
    )
)


# -----------------------------------------
# 5. CREATE DATE FEATURES
# -----------------------------------------

df["Month"] = df["Date"].dt.month

day_of_year = df["Date"].dt.dayofyear

df["Day_Sin"] = np.sin(
    2 * np.pi * day_of_year / 365
)

df["Day_Cos"] = np.cos(
    2 * np.pi * day_of_year / 365
)


# -----------------------------------------
# 6. REMOVE ROWS WITHOUT REQUIRED FEATURES
# -----------------------------------------

required_columns = [
    "PRECTOTCORR",
    "T2M",
    "T2M_MAX",
    "T2M_MIN",
    "RH2M",
    "Next_Day_Rainfall",
    "Rainfall_Lag_1",
    "Rainfall_Lag_2",
    "Rainfall_Lag_3",
    "Rainfall_3_Day_Avg"
]

df = df.dropna(
    subset=required_columns
).reset_index(drop=True)


# -----------------------------------------
# 7. SAVE HISTORICAL ML DATASET
# -----------------------------------------

Path("data").mkdir(exist_ok=True)

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# -----------------------------------------
# 8. DISPLAY DATASET INFORMATION
# -----------------------------------------

print("\nHISTORICAL ML DATA PREPARATION")
print("--------------------------------")

print("Output file:", OUTPUT_FILE)
print("Total records:", len(df))

print("Start date:", df["Date"].min())
print("End date:", df["Date"].max())

print("Districts:", df["District"].nunique())

print("\nRECORDS BY YEAR")

print(
    df.groupby(df["Date"].dt.year).size().to_string()
)

print("\nMISSING VALUES")

print(
    df[required_columns].isna().sum().to_string()
)

print("\nDATASET COLUMNS")

print(df.columns.tolist())

print("\nHistorical ML dataset created successfully!")
