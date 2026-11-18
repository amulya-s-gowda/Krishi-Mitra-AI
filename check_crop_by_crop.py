import pandas as pd

# Load crop recommendation dataset
df = pd.read_csv("data/Crop_recommendation.csv")

print("\nKRISHIMITRA AI - CROP RAINFALL ANALYSIS")
print("---------------------------------------")

# Analyze rainfall values for each crop
rainfall_analysis = df.groupby("label")["rainfall"].agg(
    ["count", "mean", "min", "max"]
)

rainfall_analysis = rainfall_analysis.round(2)

print("\nRAINFALL REQUIREMENTS BY CROP")
print(rainfall_analysis.to_string())

# Analyze other important soil features
print("\nOVERALL DATASET RANGES")

columns = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

print(
    df[columns].agg(["min", "mean", "max"]).round(2).to_string()
)

# Check for missing values
print("\nMISSING VALUES:")
print(df.isnull().sum())