
import joblib
from modules.crop_information import crop_information

# Load the trained crop model
saved_data = joblib.load(
    "crop_recommendation_model_no_rainfall.pkl"
)

model = saved_data["model"]

# Get all crop names supported by the model
model_crops = set(
    str(crop).lower() for crop in model.classes_
)

# Get crops with available farming information
available_crops = set(crop_information.keys())

# Find missing crop information
missing_crops = sorted(model_crops - available_crops)

print("\nKRISHIMITRA AI - CROP INFORMATION COVERAGE")
print("------------------------------------------")

print("Total crops supported by model:", len(model_crops))
print("Crops with information:", len(model_crops & available_crops))
print("Crops missing information:", len(missing_crops))

if missing_crops:
    print("\nMissing crop information:")
    for crop in missing_crops:
        print("-", crop)
else:
    print("\nAll crops have information!")
