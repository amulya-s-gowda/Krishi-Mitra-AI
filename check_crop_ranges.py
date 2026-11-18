
import pandas as pd

df = pd.read_csv("data/Crop_recommendation.csv")

print("\nCROP DATASET FEATURE RANGES")
print("---------------------------")

features = [
    "N", "P", "K",
    "temperature", "humidity",
    "ph", "rainfall"
]

print(df[features].describe().round(2))

print("\nCROP NAMES")
print("----------")
print(sorted(df["label"].unique()))

print("\nTOTAL CROPS:", df["label"].nunique())
