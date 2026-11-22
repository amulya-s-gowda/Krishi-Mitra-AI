
import pandas as pd
from pathlib import Path
from modules.district_data import district_coordinates

folder = Path("data/historical_2013_2025")
master_file = folder / "karnataka_master_weather_2013_2025.csv"

df = pd.read_csv(master_file)
df["Date"] = pd.to_datetime(df["Date"])

expected_dates = pd.date_range("2013-01-01", "2025-12-31")
expected_districts = set(district_coordinates.keys())

print("=" * 55)
print("KARNATAKA HISTORICAL DATA VALIDATION")
print("=" * 55)

print("Total records:", len(df))
print("Total districts:", df["District"].nunique())
print("First date:", df["Date"].min().date())
print("Last date:", df["Date"].max().date())

print("\n1. District-wise record counts:")
counts = df.groupby("District").size()
print(counts.to_string())

print("\n2. Date validation:")
print("Expected dates:", len(expected_dates))
print("Missing dates:", len(set(expected_dates) - set(df["Date"])))
print("Duplicate district-date records:",
      df.duplicated(["District", "Date"]).sum())

print("\n3. Missing values:")
print(df.isna().sum().to_string())

print("\n4. Weather value checks:")
print("Negative rainfall:",
      (df["PRECTOTCORR"] < 0).sum())
print("Invalid humidity:",
      ((df["RH2M"] < 0) | (df["RH2M"] > 100)).sum())
print("Invalid temperature ranges:",
      (df["T2M_MIN"] > df["T2M_MAX"]).sum())

print("\n5. District CSV files:")
files = list(folder.glob("*_weather.csv"))
print("Individual district files:", len(files))

# Collect validation failures
errors = []

if len(df) != 147188:
    errors.append("Incorrect total record count")

if set(df["District"].unique()) != expected_districts:
    errors.append("District list mismatch")

if len(files) != 31:
    errors.append("Expected 31 individual CSV files")

for district in expected_districts:
    district_df = df[df["District"] == district]

    if len(district_df) != 4748:
        errors.append(f"{district}: incorrect record count")

    if set(district_df["Date"]) != set(expected_dates):
        errors.append(f"{district}: missing or extra dates")

if df.duplicated(["District", "Date"]).any():
    errors.append("Duplicate district-date records")

if df.isna().any().any():
    errors.append("Missing values found")

if (df["PRECTOTCORR"] < 0).any():
    errors.append("Negative rainfall found")

if ((df["RH2M"] < 0) | (df["RH2M"] > 100)).any():
    errors.append("Invalid humidity found")

if (df["T2M_MIN"] > df["T2M_MAX"]).any():
    errors.append("Invalid temperature ranges found")

print("\n" + "=" * 55)

if errors:
    print("VALIDATION FAILED")
    for error in errors:
        print("-", error)
else:
    print("ALL VALIDATION CHECKS PASSED!")

print("=" * 55)
