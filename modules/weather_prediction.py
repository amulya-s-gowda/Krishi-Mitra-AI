
import joblib
import pandas as pd

# Load trained weather prediction model
saved_data = joblib.load("historical_weather_prediction_model.pkl")

model = saved_data["model"]
feature_columns = saved_data["feature_columns"]


def predict_next_day_rainfall(
    district,
    rainfall,
    temperature,
    max_temperature,
    min_temperature,
    humidity,
    rainfall_lag_1,
    rainfall_lag_2,
    rainfall_lag_3,
    rainfall_3_day_avg,
    month,
    day_sin,
    day_cos
):

    input_data = pd.DataFrame([{
        "PRECTOTCORR": rainfall,
        "T2M": temperature,
        "T2M_MAX": max_temperature,
        "T2M_MIN": min_temperature,
        "RH2M": humidity,
        "Rainfall_Lag_1": rainfall_lag_1,
        "Rainfall_Lag_2": rainfall_lag_2,
        "Rainfall_Lag_3": rainfall_lag_3,
        "Rainfall_3_Day_Avg": rainfall_3_day_avg,
        "Month": month,
        "Day_Sin": day_sin,
        "Day_Cos": day_cos,
        "District": district
    }])

    input_data = pd.get_dummies(input_data, columns=["District"])

    input_data = input_data.reindex(
        columns=feature_columns,
        fill_value=0
    )

    prediction = model.predict(input_data)

    return max(0, float(prediction[0]))
