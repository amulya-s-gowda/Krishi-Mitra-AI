
import requests
import pandas as pd
from datetime import date, timedelta
import math


def get_latest_weather_inputs(latitude, longitude):

    today = date.today()
    start_date = today - timedelta(days=14)

    url = "https://power.larc.nasa.gov/api/temporal/daily/point"

    parameters = {
        "parameters": "PRECTOTCORR,T2M,T2M_MAX,T2M_MIN,RH2M",
        "community": "AG",
        "longitude": longitude,
        "latitude": latitude,
        "start": start_date.strftime("%Y%m%d"),
        "end": today.strftime("%Y%m%d"),
        "format": "JSON"
    }

    # API request with 3 attempts
    last_error = None

    for attempt in range(3):
        try:
            response = requests.get(
                url,
                params=parameters,
                timeout=60
            )
            response.raise_for_status()
            break

        except requests.RequestException as error:
            last_error = error

    else:
        raise ConnectionError(
            f"NASA weather API unavailable after 3 attempts: {last_error}"
        )

    # Read API response
    weather_json = response.json()
    weather_data = weather_json["properties"]["parameter"]

    df = pd.DataFrame(weather_data)
    df.index.name = "Date"
    df = df.reset_index()

    df["Date"] = pd.to_datetime(df["Date"], format="%Y%m%d")

    weather_columns = [
        "PRECTOTCORR", "T2M", "T2M_MAX", "T2M_MIN", "RH2M"
    ]

    for column in weather_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.replace(-999, float("nan"))
    df = df.sort_values("Date").set_index("Date")

    # Find latest valid weather record
    valid_dates = df.dropna(subset=weather_columns).index

    if len(valid_dates) == 0:
        raise ValueError("No valid weather data is available.")

    latest_date = valid_dates[-1]

    # Get latest date and previous 3 days
    required_dates = pd.date_range(
        end=latest_date,
        periods=4,
        freq="D"
    )

    if not all(current_date in df.index for current_date in required_dates):
        raise ValueError(
            "Weather data for the previous three days is incomplete."
        )

    recent = df.loc[required_dates]

    if recent[weather_columns].isna().any().any():
        raise ValueError(
            "Some required weather values are missing."
        )

    current = recent.iloc[-1]

    rainfall_lag_1 = float(recent.iloc[-2]["PRECTOTCORR"])
    rainfall_lag_2 = float(recent.iloc[-3]["PRECTOTCORR"])
    rainfall_lag_3 = float(recent.iloc[-4]["PRECTOTCORR"])

    rainfall_average = (
        rainfall_lag_1 +
        rainfall_lag_2 +
        rainfall_lag_3
    ) / 3

    day_of_year = latest_date.dayofyear

    day_sin = math.sin(2 * math.pi * day_of_year / 365)
    day_cos = math.cos(2 * math.pi * day_of_year / 365)

    return {
        "weather_date": latest_date.date(),
        "prediction_date": (latest_date + timedelta(days=1)).date(),

        "rainfall": float(current["PRECTOTCORR"]),
        "temperature": float(current["T2M"]),
        "max_temperature": float(current["T2M_MAX"]),
        "min_temperature": float(current["T2M_MIN"]),
        "humidity": float(current["RH2M"]),

        "rainfall_lag_1": rainfall_lag_1,
        "rainfall_lag_2": rainfall_lag_2,
        "rainfall_lag_3": rainfall_lag_3,
        "rainfall_3_day_avg": rainfall_average,

        "month": latest_date.month,
        "day_sin": day_sin,
        "day_cos": day_cos
    }
