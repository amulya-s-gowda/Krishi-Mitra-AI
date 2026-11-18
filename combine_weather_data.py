
import pandas as pd
import glob
import os

# Folder containing all district CSV files
data_folder = "data"

# Find all weather CSV files
csv_files = glob.glob(os.path.join(data_folder, "*_weather.csv"))

print(f"Found {len(csv_files)} weather files.")

if not csv_files:
    print("No weather files found. Please check your data folder.")

else:
    all_district_data = []

    # Read each district file
    for file in csv_files:
        try:
            df = pd.read_csv(file)

            if "District" not in df.columns:
                print(f"Skipping {file}: District column is missing.")
                continue

            all_district_data.append(df)
            print(f"Loaded: {file}")

        except Exception as error:
            print(f"Error reading {file}: {error}")

    if all_district_data:
        # Combine all district datasets
        master_df = pd.concat(all_district_data, ignore_index=True)

        # Convert Date column into proper date format
        master_df["Date"] = pd.to_datetime(master_df["Date"])

        # Remove duplicate district-date records
        master_df = master_df.drop_duplicates(
            subset=["District", "Date"]
        )

        # Sort by district and date
        master_df = master_df.sort_values(
            by=["District", "Date"]
        )

        # Save the master dataset
        output_path = os.path.join(
            data_folder, "karnataka_master_weather.csv"
        )

        master_df.to_csv(output_path, index=False)

        print("\nMaster dataset created successfully!")
        print("Total records:", len(master_df))
        print("Total districts:", master_df["District"].nunique())
        print("Columns:", list(master_df.columns))
        print("\nFirst five records:")
        print(master_df.head())

        print("\nMissing values:")
        print(master_df.isnull().sum())

    else:
        print("No valid district datasets could be combined.")
