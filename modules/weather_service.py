
from datetime import date

from modules.district_data import district_coordinates
from modules.weather_data import get_latest_weather_inputs
from modules.weather_prediction import predict_next_day_rainfall


def get_district_weather_prediction(district):

    if district not in district_coordinates:
        raise ValueError(f"District not found: {district}")

    latitude, longitude = district_coordinates[district]

    # Get the latest available weather data
    weather = get_latest_weather_inputs(latitude, longitude)

    # Remove date information before sending inputs to the ML model
    model_inputs = {
        key: value
        for key, value in weather.items()
        if key not in ["weather_date", "prediction_date"]
    }

    # Predict next-day rainfall
    predicted_rainfall = predict_next_day_rainfall(
        district=district,
        **model_inputs
    )

    # Calculate how old the weather data is
    data_age = (date.today() - weather["weather_date"]).days

    # Check whether the data is recent enough
    is_recent = data_age <= 1

    if is_recent:
        status_message = "Weather data is recent."
    else:
        status_message = (
            "Weather data is delayed. "
            "This prediction should not be treated as a current forecast."
        )

    return {
        "district": district,
        "weather_date": weather["weather_date"],
        "prediction_date": weather["prediction_date"],
        "data_age_days": data_age,
        "is_recent": is_recent,
        "status_message": status_message,
        "predicted_rainfall": predicted_rainfall,
        "weather_inputs": weather
    }
