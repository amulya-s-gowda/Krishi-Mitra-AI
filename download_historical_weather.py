
import time
import requests
import pandas as pd
from pathlib import Path

from modules.district_data import district_coordinates


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

START_DATE = "20130101"
END_DATE = "20251231"

PARAMETERS = "PRECTOTCORR,T2M,T2M_MAX,T2M_MIN,RH2M"

OUTPUT_FILE = Path("data/karnataka_weather_2013_2025.csv")
CHECKPOINT_FILE = Path("data/karnataka_weather_2013_2025_partial.csv")

WEATHER_COLUMNS = [
    "PRECTOTCORR",
    "T2M",
    "T2M_MAX",
    "T2M_MIN",
    "RH2M"
]

EXPECTED_DATES = pd.date_range(
    start="2013-01-01",
    end="2025-12-31",
    freq="D"
)


# --------------------------------------------------
# DOWNLOAD ONE DISTRICT
# --------------------------------------------------

def download_district(district, latitude, longitude):

    params = {
        "parameters": PARAMETERS,
        "community": "AG",
        "longitude": longitude,
        "latitude": latitude,
        "start": START_DATE,
        "end": END_DATE,
        "format": "JSON"
    }

    for attempt in range(3):

        try:
            response = requests.get(
                BASE_URL,
                params=params,
                timeout=120
            )

            response.raise_for_status()

            weather_json = response.json()

            weather_data = weather_json[
                "properties"
            ]["parameter"]

            df = pd.DataFrame(weather_data)

            df.index.name = "Date"
            df = df.reset_index()

            df["Date"] = pd.to_datetime(
                df["Date"],
                format="%Y%m%d"
            )

            for column in WEATHER_COLUMNS:
                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce"
                )

            df = df.replace(-999, float("nan"))

            df["District"] = district

            df = df[
                ["Date", "District"] + WEATHER_COLUMNS
            ]

            df = df.sort_values("Date")

            # Check daily date coverage
            actual_dates = pd.DatetimeIndex(
                df["Date"].drop_duplicates().sort_values()
            )

            if not actual_dates.equals(EXPECTED_DATES):
                raise ValueError(
                    f"Incomplete date coverage for {district}. "
                    f"Received {len(actual_dates)} dates; "
                    f"expected {len(EXPECTED_DATES)}."
                )

            return df

        except Exception as error:

            print(
                f"Attempt {attempt + 1}/3 failed for "
                f"{district}: {error}"
            )

            if attempt < 2:
                time.sleep(3 * (attempt + 1))

    raise RuntimeError(
        f"Could not download historical data for {district}"
    )


# --------------------------------------------------
# MAIN DOWNLOAD PROCESS
# --------------------------------------------------

def main():

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if CHECKPOINT_FILE.exists():

        all_data = pd.read_csv(
            CHECKPOINT_FILE,
            parse_dates=["Date"]
        )

        print("Existing checkpoint found.")

    else:

        all_data = pd.DataFrame(
            columns=["Date", "District"] + WEATHER_COLUMNS
        )

    districts = list(district_coordinates.items())

    print("\nKARNATAKA HISTORICAL WEATHER DOWNLOAD")
    print("--------------------------------------")
    print("Period: 2013 to 2025")
    print("Districts:", len(districts))
    print("Expected dates per district:", len(EXPECTED_DATES))
    print("Expected total records:", len(districts) * len(EXPECTED_DATES))

    for index, (district, coordinates) in enumerate(
        districts, start=1
    ):

        existing = all_data[
            all_data["District"] == district
        ].copy()

        if not existing.empty:

            existing_dates = pd.DatetimeIndex(
                existing["Date"].drop_duplicates().sort_values()
            )

            complete = (
                existing_dates.equals(EXPECTED_DATES)
                and not existing[WEATHER_COLUMNS].isna().any().any()
            )

            if complete:
                print(
                    f"[{index}/{len(districts)}] "
                    f"{district}: already complete, skipping."
                )
                continue

        latitude, longitude = coordinates

        print(
            f"\n[{index}/{len(districts)}] "
            f"Downloading {district}..."
        )

        district_data = download_district(
            district,
            latitude,
            longitude
        )

        # Replace this district's old checkpoint data
        all_data = all_data[
            all_data["District"] != district
        ]

        all_data = pd.concat(
            [all_data, district_data],
            ignore_index=True
        )

        all_data = all_data.sort_values(
            ["District", "Date"]
        )

        # Save progress after every district
        all_data.to_csv(
            CHECKPOINT_FILE,
            index=False
        )

        print(
            f"Saved {len(district_data)} records for {district}."
        )

        # Avoid sending requests too quickly
        time.sleep(2)

    # --------------------------------------------------
    # FINAL VALIDATION
    # --------------------------------------------------

    all_data = all_data.drop_duplicates(
        subset=["District", "Date"]
    )

    all_data = all_data.sort_values(
        ["District", "Date"]
    ).reset_index(drop=True)

    incomplete_districts = []

    for district, _ in districts:

        district_df = all_data[
            all_data["District"] == district
        ]

        dates = pd.DatetimeIndex(
            district_df["Date"].drop_duplicates().sort_values()
        )

        if (
            not dates.equals(EXPECTED_DATES)
            or district_df[WEATHER_COLUMNS].isna().any().any()
        ):
            incomplete_districts.append(district)

    if incomplete_districts:

        print("\nVALIDATION WARNING")
        print("Some districts have incomplete data:")
        print(incomplete_districts)
        print("Checkpoint retained. Run the script again to retry.")

        return

    all_data.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nDOWNLOAD COMPLETED SUCCESSFULLY")
    print("--------------------------------")
    print("Output file:", OUTPUT_FILE)
    print("Total records:", len(all_data))
    print("Districts:", all_data["District"].nunique())
    print("Start date:", all_data["Date"].min())
    print("End date:", all_data["Date"].max())
    print("Missing values:", all_data[WEATHER_COLUMNS].isna().sum().sum())


if __name__ == "__main__":
    main()
