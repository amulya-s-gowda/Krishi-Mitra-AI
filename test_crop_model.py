
import pickle
import pandas as pd

# Load saved model
with open("crop_recommendation_model.pkl", "rb") as file:
    saved_data = pickle.load(file)

# Extract actual model
model = saved_data["model"]

# Get feature columns used during training
feature_columns = saved_data["feature_columns"]

# Sample input values
sample_data = pd.DataFrame([{
    "N": 90,
    "P": 42,
    "K": 43,
    "temperature": 23.5,
    "humidity": 82.0,
    "ph": 6.5,
    "rainfall": 220.0
}])

# Arrange input columns in training order
sample_data = sample_data[feature_columns]

# Predict crop
prediction = model.predict(sample_data)

print("\nKRISHIMITRA AI - CROP RECOMMENDATION")
print("-----------------------------------")
print("Recommended Crop:", prediction[0].upper())
