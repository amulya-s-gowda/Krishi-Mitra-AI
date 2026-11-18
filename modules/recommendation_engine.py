
from models.crop_recommendation import recommend_crop
from modules.weather_prediction import predict_next_day_rainfall


def get_krishimitra_recommendations(
    district,
    weather_inputs,
    soil_inputs
):
    # Predict next-day rainfall
    predicted_rainfall = predict_next_day_rainfall(
        district=district,
        **weather_inputs
    )

    # Recommend crop using soil and crop-growing conditions
    crop = recommend_crop(
        n=soil_inputs["N"],
        p=soil_inputs["P"],
        k=soil_inputs["K"],
        temperature=soil_inputs["temperature"],
        humidity=soil_inputs["humidity"],
        ph=soil_inputs["ph"],
        rainfall=soil_inputs["rainfall"]
    )

    return {
        "district": district,
        "predicted_rainfall": predicted_rainfall,
        "recommended_crop": crop
    }
