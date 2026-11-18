
import joblib
import pandas as pd

MODEL_PATH = "crop_recommendation_model_no_rainfall.pkl"

saved_data = joblib.load(MODEL_PATH)

model = saved_data["model"]
feature_columns = saved_data["feature_columns"]


def get_all_crop_predictions(n, p, k, temperature, humidity, ph):

    input_data = pd.DataFrame([{
        "N": n,
        "P": p,
        "K": k,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph
    }])

    input_data = input_data[feature_columns]

    probabilities = model.predict_proba(input_data)[0]

    predictions = []

    for index, probability in enumerate(probabilities):
        predictions.append({
            "crop": str(model.classes_[index]).lower().strip(),
            "confidence": round(float(probability) * 100, 2)
        })

    return predictions


# Original function retained for compatibility
def recommend_crop_without_rainfall(n, p, k, temperature, humidity, ph):

    predictions = get_all_crop_predictions(
        n, p, k, temperature, humidity, ph
    )

    predictions.sort(
        key=lambda item: item["confidence"],
        reverse=True
    )

    return predictions[:3]


# New district-aware ML recommendation function
def recommend_crop_with_soil_report(
    n, p, k, temperature, humidity, ph,
    district, soil, season
):

    from modules.crop_recommendation_without_soil_test import (
        SOIL_SUITABILITY,
        SEASON_SUITABILITY,
        DISTRICT_CROP_PROFILE
    )

    # Get predictions for all crops
    predictions = get_all_crop_predictions(
        n, p, k, temperature, humidity, ph
    )

    # Get crops supported by the selected district
    district_crops = {
        crop.lower() for crop in DISTRICT_CROP_PROFILE.get(
            district, []
        )
    }

    soil_crops = {
        crop.lower() for crop in SOIL_SUITABILITY.get(
            soil, []
        )
    }

    season_crops = {
        crop.lower() for crop in SEASON_SUITABILITY.get(
            season, []
        )
    }

    # Keep only crops supported by the district
    eligible_crops = []

    for item in predictions:

        crop = item["crop"]

        if crop not in district_crops:
            continue

        soil_match = crop in soil_crops
        season_match = crop in season_crops

        # Suitability score is separate from ML confidence
        suitability_score = (
            (2 if soil_match else 0)
            + (2 if season_match else 0)
        )

        item["soil_match"] = soil_match
        item["season_match"] = season_match
        item["district_match"] = True
        item["suitability_score"] = suitability_score

        eligible_crops.append(item)

       # Rank by ML confidence first.
    # Use soil and season suitability as tie-breakers.
    eligible_crops.sort(
        key=lambda item: (
            -item["confidence"],
            -item["suitability_score"]
        )
    )

    # Separate crops with positive ML scores
    positive_predictions = [
        item for item in eligible_crops
        if item["confidence"] > 0
    ]

    # Return up to 3 eligible crops
    return positive_predictions[:3] + [
        item for item in eligible_crops
        if item["confidence"] == 0
    ][:max(0, 3 - len(positive_predictions))]
