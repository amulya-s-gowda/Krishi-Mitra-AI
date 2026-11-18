from modules.weather_data import get_latest_weather_inputs
from modules.weather_prediction import predict_next_day_rainfall

# Shivamogga district
district = "Shivamogga"

latitude = 13.9299
longitude = 75.5681

try:
    # Step 1: Get recent weather inputs
    weather = get_latest_weather_inputs(latitude, longitude)

    # Step 2: Remove date fields (the model does not need them)
    model_inputs = {
        key: value
        for key, value in weather.items()
        if key not in ["weather_date", "prediction_date"]
    }

    # Step 3: Predict rainfall
    predicted_rainfall = predict_next_day_rainfall(
        district=district,
        **model_inputs
    )

    # Step 4: Display result
    print("\nKRISHIMITRA AI - WEATHER PREDICTION")
    print("-----------------------------------")
    print("District:", district)
    print("Weather data date:", weather["weather_date"])
    print("Prediction date:", weather["prediction_date"])
    print(f"Predicted rainfall: {predicted_rainfall:.2f} mm")

except Exception as error:
    print("\nError:", error)
    