
import pickle
import pandas as pd

# Load the trained crop recommendation model
with open("crop_recommendation_model.pkl", "rb") as file:
    saved_data = pickle.load(file)

model = saved_data["model"]
feature_columns = saved_data["feature_columns"]


def recommend_crop(n, p, k, temperature, humidity, ph, rainfall):

    input_data = pd.DataFrame([{
        "N": n,
        "P": p,
        "K": k,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall
    }])

    input_data = input_data[feature_columns]

    prediction = model.predict(input_data)

    return prediction[0]
