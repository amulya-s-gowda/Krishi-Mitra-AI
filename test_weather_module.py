
from modules.weather_prediction import predict_next_day_rainfall

rainfall = predict_next_day_rainfall(
    district="Shivamogga",
    rainfall=5.0,
    temperature=25.0,
    max_temperature=29.0,
    min_temperature=21.0,
    humidity=80.0,
    rainfall_lag_1=5.0,
    rainfall_lag_2=2.0,
    rainfall_lag_3=0.0,
    rainfall_3_day_avg=2.33,
    month=11,
    day_sin=0.0,
    day_cos=1.0
)

print("\nKRISHIMITRA AI - WEATHER PREDICTION")
print("-----------------------------------")
print("District: Shivamogga")
print("Predicted next-day rainfall:", round(rainfall, 2), "mm")
