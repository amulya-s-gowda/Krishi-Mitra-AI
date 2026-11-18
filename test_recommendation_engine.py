
from modules.recommendation_engine import get_krishimitra_recommendations

weather_inputs = {
    "rainfall": 5.0,
    "temperature": 25.0,
    "max_temperature": 29.0,
    "min_temperature": 21.0,
    "humidity": 80.0,
    "rainfall_lag_1": 5.0,
    "rainfall_lag_2": 2.0,
    "rainfall_lag_3": 0.0,
    "rainfall_3_day_avg": 2.33,
    "month": 11,
    "day_sin": 0.0,
    "day_cos": 1.0
}

soil_inputs = {
    "N": 90,
    "P": 42,
    "K": 43,
    "temperature": 23.5,
    "humidity": 82.0,
    "ph": 6.5,
    "rainfall": 220.0
}

result = get_krishimitra_recommendations(
    district="Shivamogga",
    weather_inputs=weather_inputs,
    soil_inputs=soil_inputs
)

print("\nKRISHIMITRA AI")
print("------------------------------")
print("District:", result["district"])
print(
    "Predicted next-day rainfall:",
    round(result["predicted_rainfall"], 2),
    "mm"
)
print("Recommended crop:", result["recommended_crop"].upper())
