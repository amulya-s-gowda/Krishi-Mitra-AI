
# Rule-based crop recommendation for farmers
# who do not have a soil test report.

SOIL_SUITABILITY = {
    "Red Soil": [
        "maize", "pigeonpeas", "blackgram",
        "mungbean", "cotton", "chickpea",
        "ragi", "groundnut"
    ],

    "Black Soil": [
        "cotton", "chickpea", "pigeonpeas",
        "maize", "lentil", "blackgram"
    ],

    "Alluvial Soil": [
        "rice", "maize", "banana",
        "jute", "mungbean", "blackgram",
        "ragi"
    ],

    "Laterite Soil": [
        "coffee", "coconut", "banana",
        "blackgram", "pigeonpeas", "ragi"
    ],

    "Clay Soil": [
        "rice", "cotton", "chickpea",
        "lentil", "maize", "pigeonpeas"
    ]
}

SEASON_SUITABILITY = {
    "Kharif": [
        "rice", "maize", "cotton", "jute",
        "pigeonpeas", "blackgram", "mungbean",
        "mothbeans", "banana", "ragi",
        "groundnut", "horsegram"
    ],

    "Rabi": [
        "chickpea", "lentil", "kidneybeans",
        "pigeonpeas", "maize", "blackgram",
        "ragi", "horsegram"
    ],

    "Summer": [
        "watermelon", "muskmelon", "mungbean",
        "maize", "banana", "papaya"
    ]
}



# District crop profiles.
# These lists represent crops documented as cultivated
# in the district. They are not farm-level guarantees.


# District crop profiles based on documented district-level
# crop cultivation records. These are not farm-level guarantees.

DISTRICT_CROP_PROFILE = {

        "Bagalkote": [
        "maize", "pigeonpeas", "chickpea",
        "mungbean", "blackgram", "cotton",
        "groundnut"
    ],

        "Bengaluru Rural": [
        "maize", "pigeonpeas", "ragi",
        "groundnut", "horsegram",
        "mungbean", "chickpea"
    ],

        "Kolar": [
        "pigeonpeas", "ragi",
        "groundnut", "horsegram",
        "maize", "chickpea"
    ],

    "Mysuru": [
        "rice", "maize", "pigeonpeas",
        "blackgram", "mungbean", "chickpea",
        "cotton", "banana", "papaya",
        "ragi", "groundnut", "horsegram"
    ],
        "Shivamogga": [
        "rice", "maize", "ragi",
        "groundnut", "pigeonpeas",
        "blackgram", "mungbean",
        "chickpea", "cotton", "banana"
    ],
    "Tumakuru": [
        "rice", "maize", "ragi", "pigeonpeas",
        "horsegram", "blackgram", "mungbean",
        "groundnut"
    ],
}



def recommend_crops_without_soil_test(soil, season, district=None):

    if soil not in SOIL_SUITABILITY:
        raise ValueError("Invalid soil type")

    if season not in SEASON_SUITABILITY:
        raise ValueError("Invalid farming season")

    soil_crops = SOIL_SUITABILITY[soil]
    season_crops = SEASON_SUITABILITY[season]

    district_crops = DISTRICT_CROP_PROFILE.get(district)

    all_candidates = set(soil_crops + season_crops)

    recommendations = []

    for crop in all_candidates:

        score = 0
        reasons = []

        soil_match = crop in soil_crops
        season_match = crop in season_crops

        district_match = (
            crop in district_crops
            if district_crops is not None
            else None
        )

        if soil_match:
            score += 2
            reasons.append("Selected soil type")

        if season_match:
            score += 2
            reasons.append("Selected farming season")

        if district_match is True:
            reasons.append("Cultivated in selected district")

        if score > 0:

            recommendations.append({
                "crop": crop,
                "score": score,
                "soil_match": soil_match,
                "season_match": season_match,
                "district_match": district_match,
                "reasons": reasons
            })

    # First: soil and season score.
    # Second: crops documented in the selected district.
    # Third: alphabetical order for consistent results.

    recommendations.sort(
        key=lambda item: (
            -item["score"],
            item["district_match"] is not True,
            item["crop"]
        )
    )

    return recommendations[:3]
