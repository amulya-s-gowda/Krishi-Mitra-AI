
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load prepared dataset
df = pd.read_csv("data/weather_prediction_dataset.csv")

df["Date"] = pd.to_datetime(df["Date"])

# Define input features
features = [
    "PRECTOTCORR",
    "T2M",
    "T2M_MAX",
    "T2M_MIN",
    "RH2M",
    "Rainfall_Lag_1",
    "Rainfall_Lag_2",
    "Rainfall_Lag_3",
    "Rainfall_3_Day_Avg",
    "Month",
    "Day_Sin",
    "Day_Cos",
    "District"
]

target = "Next_Day_Rainfall"

# Convert district names into numerical columns
X = pd.get_dummies(df[features], columns=["District"], dtype=int)
y = df[target]

# Chronological split:
# Train on 2023 and 2024
# Test on 2025
train_mask = df["Date"].dt.year < 2025
test_mask = df["Date"].dt.year == 2025

X_train = X.loc[train_mask]
X_test = X.loc[test_mask]

y_train = y.loc[train_mask]
y_test = y.loc[test_mask]

print("DATA SPLITTING")
print("----------------")
print("Training records:", len(X_train))
print("Testing records:", len(X_test))

# Create Random Forest model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

# Train model
print("\nTraining Random Forest model...")
model.fit(X_train, y_train)

# Predict rainfall
predictions = model.predict(X_test)

# Evaluate model
mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions) ** 0.5
r2 = r2_score(y_test, predictions)

print("\nMODEL EVALUATION")
print("----------------")
print("MAE:", round(mae, 3), "mm")
print("RMSE:", round(rmse, 3), "mm")
print("R2 Score:", round(r2, 3))

# Save model and feature columns
joblib.dump(
    {
        "model": model,
        "feature_columns": X.columns.tolist()
    },
    "weather_prediction_model.pkl"
)

print("\nModel saved successfully!")
print("File: weather_prediction_model.pkl")
