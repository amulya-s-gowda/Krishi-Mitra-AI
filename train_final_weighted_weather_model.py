
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load prepared dataset
df = pd.read_csv("data/weather_prediction_dataset.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Input features
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

# Prepare features
X = pd.get_dummies(
    df[features],
    columns=["District"],
    dtype=int
)

y = df[target]

# Chronological split
train_mask = df["Date"].dt.year < 2025
test_mask = df["Date"].dt.year == 2025

X_train = X.loc[train_mask]
X_test = X.loc[test_mask]

y_train = y.loc[train_mask]
y_test = y.loc[test_mask]

# Selected weight from validation experiment
HEAVY_RAINFALL_THRESHOLD = 15
HEAVY_RAINFALL_WEIGHT = 4

sample_weights = y_train.apply(
    lambda rainfall: HEAVY_RAINFALL_WEIGHT
    if rainfall >= HEAVY_RAINFALL_THRESHOLD
    else 1
)

print("FINAL WEIGHTED MODEL TRAINING")
print("-----------------------------")
print("Training records:", len(X_train))
print("Testing records:", len(X_test))
print("Heavy rainfall weight:", HEAVY_RAINFALL_WEIGHT)
print(
    "Heavy rainfall training records:",
    int((y_train >= HEAVY_RAINFALL_THRESHOLD).sum())
)

# Train Random Forest
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

print("\nTraining model...")

model.fit(
    X_train,
    y_train,
    sample_weight=sample_weights
)

# Predict 2025 rainfall
predictions = model.predict(X_test)

# Overall performance
print("\nOVERALL MODEL PERFORMANCE")
print("--------------------------")

print("MAE:", round(mean_absolute_error(y_test, predictions), 3))
print("RMSE:", round(mean_squared_error(y_test, predictions) ** 0.5, 3))
print("R2:", round(r2_score(y_test, predictions), 3))

# Heavy rainfall evaluation
heavy_mask = y_test >= HEAVY_RAINFALL_THRESHOLD

actual_heavy = y_test[heavy_mask]
predicted_heavy = predictions[heavy_mask]

print("\nHEAVY RAINFALL PERFORMANCE")
print("--------------------------")

print("Records:", len(actual_heavy))
print("Average actual:", round(actual_heavy.mean(), 2), "mm")
print("Average predicted:", round(predicted_heavy.mean(), 2), "mm")
print(
    "Average prediction error:",
    round((predicted_heavy - actual_heavy).mean(), 2),
    "mm"
)
print(
    "Underpredicted records:",
    int((predicted_heavy < actual_heavy).sum())
)
print(
    "Predictions below half actual:",
    int((predicted_heavy < actual_heavy * 0.5).sum())
)

# Evaluate all rainfall categories
categories = [
    ("No rain", y_test < 0.1),
    ("Very light rain", (y_test >= 0.1) & (y_test < 2.5)),
    ("Light to moderate", (y_test >= 2.5) & (y_test < 15)),
    ("Heavy rainfall", y_test >= 15)
]

print("\nERROR BY RAINFALL CATEGORY")
print("--------------------------")

for category, mask in categories:
    if mask.sum() > 0:
        category_mae = mean_absolute_error(
            y_test[mask],
            predictions[mask]
        )

        print(
            category,
            "| Records:", int(mask.sum()),
            "| MAE:", round(category_mae, 3), "mm"
        )

# Save predictions separately
test_df = df.loc[test_mask].copy()
test_df["Predicted_Rainfall"] = predictions
test_df["Prediction_Error"] = (
    predictions - y_test.to_numpy()
)

test_df.to_csv(
    "data/final_weighted_weather_predictions.csv",
    index=False
)

# Save model and feature columns separately
joblib.dump(
    {
        "model": model,
        "feature_columns": X.columns.tolist()
    },
    "final_weighted_weather_prediction_model.pkl"
)

print("\nFinal experimental model saved successfully!")
print("Model: final_weighted_weather_prediction_model.pkl")
print("Predictions: data/final_weighted_weather_predictions.csv")
