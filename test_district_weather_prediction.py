
from modules.weather_service import get_district_weather_prediction

selected_district = "Mysuru"

try:
    result = get_district_weather_prediction(selected_district)

    print("\nKRISHIMITRA AI - DISTRICT WEATHER REPORT")
    print("---------------------------------------")

    print("District:", result["district"])
    print("Weather data date:", result["weather_date"])
    print("Prediction date:", result["prediction_date"])
    print("Data age:", result["data_age_days"], "days")

    print("Data status:",
          "Recent" if result["is_recent"] else "Outdated")

    print("Status message:", result["status_message"])

    if result["is_recent"]:
        print(
            "Predicted rainfall:",
            round(result["predicted_rainfall"], 2),
            "mm"
        )
    else:
        print("Current forecast: Not available due to delayed data.")

        print(
            "Historical model estimate:",
            round(result["predicted_rainfall"], 2),
            "mm"
        )

except Exception as error:
    print("Error:", error)
