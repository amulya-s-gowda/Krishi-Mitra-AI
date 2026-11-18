from models.crop_recommendation_no_rainfall import (
    recommend_crop_without_rainfall
)

result = recommend_crop_without_rainfall(
    n=90,
    p=42,
    k=43,
    temperature=22.83,
    humidity=66.49,
    ph=6.5
)

print("\nKRISHIMITRA AI - TOP 3 CROP RECOMMENDATIONS")
print("-------------------------------------------")

for i, crop in enumerate(result, start=1):
    print(f"{i}. {crop['crop'].upper()}")
    print(f"   Model confidence: {crop['confidence']}%")