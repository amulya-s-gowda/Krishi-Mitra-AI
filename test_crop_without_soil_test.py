
from modules.crop_recommendation_without_soil_test import (
    recommend_crops_without_soil_test
)

result = recommend_crops_without_soil_test(
    soil="Red Soil",
    season="Kharif"
)

print("\nKRISHIMITRA AI")
print("CROP RECOMMENDATIONS WITHOUT SOIL TEST")
print("--------------------------------------")

for i, crop in enumerate(result, start=1):
    print(f"{i}. {crop['crop'].upper()}")
    print(f"   Rule score: {crop['score']}/4")
    print("   Soil match:", crop["soil_match"])
print("   Season match:", crop["season_match"])
print("   Reasons:", ", ".join(crop["reasons"]))
