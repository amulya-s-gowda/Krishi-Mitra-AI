
import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned dataset
df = pd.read_csv("data/karnataka_weather_cleaned.csv")

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"])

# Extract year and month
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month

print("DATASET OVERVIEW")
print("----------------")
print("Total records:", len(df))
print("Total districts:", df["District"].nunique())
print("Date range:", df["Date"].min(), "to", df["Date"].max())

# --------------------------------
# GRAPH 1: Average annual rainfall
# --------------------------------

annual_rainfall = (
    df.groupby(["District", "Year"])["PRECTOTCORR"]
    .sum()
    .reset_index()
)

average_rainfall = (
    annual_rainfall.groupby("District")["PRECTOTCORR"]
    .mean()
    .sort_values(ascending=False)
)

plt.figure(figsize=(14, 7))
average_rainfall.plot(kind="bar")
plt.title("Average Annual Rainfall by District")
plt.xlabel("District")
plt.ylabel("Rainfall (mm)")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("data/rainfall_by_district.png")
plt.show()

# --------------------------------
# GRAPH 2: Average temperature
# --------------------------------

temperature = (
    df.groupby("District")["T2M"]
    .mean()
    .sort_values(ascending=False)
)

plt.figure(figsize=(14, 7))
temperature.plot(kind="bar")
plt.title("Average Temperature by District")
plt.xlabel("District")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("data/temperature_by_district.png")
plt.show()

# --------------------------------
# GRAPH 3: Monthly rainfall pattern
# --------------------------------

monthly_rainfall = df.groupby("Month")["PRECTOTCORR"].mean()

month_names = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

plt.figure(figsize=(11, 5))
monthly_rainfall.plot(kind="bar")
plt.title("Average Daily Rainfall Across Karnataka by Month")
plt.xlabel("Month")
plt.ylabel("Average Rainfall (mm/day)")
plt.xticks(
    ticks=range(12),
    labels=month_names,
    rotation=0
)
plt.tight_layout()
plt.savefig("data/monthly_rainfall.png")
plt.show()

print("\nAll graphs generated successfully!")
