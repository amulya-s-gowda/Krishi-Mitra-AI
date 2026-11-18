import pandas as pd

file_path = "data/Crop_recommendation.csv"

df = pd.read_csv(file_path)

print("\nCROP DATASET DETAILS")
print("--------------------")

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 10 records:")
print(df.head(10).to_string(index=False))

print("\nDataset information:")
print(df.info())

print("\nRainfall statistics:")
print(df["rainfall"].describe())

print("\nUnique crop names:")
print(sorted(df["label"].unique()))