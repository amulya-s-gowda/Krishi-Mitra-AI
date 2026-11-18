
from modules.weather_service import get_district_weather_prediction

districts = [
    "Bagalkote",
    "Bengaluru Urban",
"Bengaluru Rural",
"Bengaluru South",
    "Mysuru",
    "Udupi",
    "Uttara Kannada",
    "Kalaburagi"
]

print("\nKRISHIMITRA AI - DISTRICT WEATHER TEST")
print("=" * 45)

for district in districts:

    print(f"\nTesting: {district}")
    print("-" * 40)

    try:
        result = get_district_weather_prediction(district)
        weather = result["weather_inputs"]

        print("Weather data date:", result["weather_date"])
        print("Prediction date:", result["prediction_date"])
        print("Data age:", result["data_age_days"], "days")
        print("Data status:", result["status_message"])

        print("Recorded rainfall:", round(weather["rainfall"], 2), "mm")
        print("Temperature:", round(weather["temperature"], 2), "°C")
        print("Maximum temperature:", round(weather["max_temperature"], 2), "°C")
        print("Minimum temperature:", round(weather["min_temperature"], 2), "°C")
        print("Humidity:", round(weather["humidity"], 2), "%")

        print(
            "Predicted next-day rainfall:",
            round(result["predicted_rainfall"], 2),
            "mm"
        )

        print("Result: SUCCESS")

    except Exception as e:
        print("Result: FAILED")
        print("Error:", str(e))

print("\n" + "=" * 45)
print("DISTRICT TESTING COMPLETED")
