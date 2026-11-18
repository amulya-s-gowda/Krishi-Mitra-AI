
import pandas as pd

CLIMATE_FILE = "data/district_season_climate.csv"


def get_seasonal_climate(district, season):

    df = pd.read_csv(CLIMATE_FILE)

    # Find the selected district and season
    result = df[
        (df["District"] == district) &
        (df["Season"] == season)
    ]

    if result.empty:
        raise ValueError(
            f"Climate information not found for {district} - {season}"
        )

    climate = result.iloc[0]

    return {
        "rainfall": float(climate["Average_Rainfall"]),
        "temperature": float(climate["Average_Temperature"]),
        "humidity": float(climate["Average_Humidity"])
    }
