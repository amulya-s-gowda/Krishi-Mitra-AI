
from modules.crop_recommendation_without_soil_test import (
    recommend_crops_without_soil_test
)

soil_types = [
    "Red Soil",
    "Black Soil",
    "Alluvial Soil",
    "Laterite Soil",
    "Clay Soil"
]

seasons = [
    "Kharif",
    "Rabi",
    "Summer"
]

print("\nKRISHIMITRA AI")
print("CROP RECOMMENDATION TEST")
print("=" * 50)

for soil in soil_types:

    for season in seasons:

        result = recommend_crops_without_soil_test(
            soil=soil,
            season=season
        )

        print(f"\nSoil: {soil}")
        print(f"Season: {season}")

        for i, crop in enumerate(result, start=1):
            print(
                f"{i}. {crop['crop'].upper()} "
                f"({crop['score']}/4)"
            )

        if len(result) == 3:
            print("Test: PASSED")
        else:
            print("Test: FAILED")

print("\nAll combinations tested.")
