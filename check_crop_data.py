
import pandas as pd

# Load crop dataset
df = pd.read_csv("data/Crop_recommendation.csv")

print("CROP DATASET OVERVIEW")
print("---------------------")

print("Total records:", len(df))
print("Total columns:", len(df.columns))

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst five records:")
print(df.head())

print("\nAvailable crops:")
print(df["label"].unique())

print("\nMissing values:")
print(df.isnull().sum())
