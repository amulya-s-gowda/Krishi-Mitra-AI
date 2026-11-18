
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

# Chronological train-test split
train_mask = df["Date"].dt.year < 2025
test_mask = df["Date"].dt.year == 2025

X = pd.get_dummies(
    df[features],
    columns=["District"],
    dtype=int
)

y = df[target]

X_train = X.loc[train_mask]
X_test = X.loc[test_mask]

y_train = y.loc[train_mask]
y_test = y.loc[test_mask]

# Assign higher weight to heavy-rainfall training records
sample_weights = y_train.apply(
    lambda rainfall: 3 if rainfall >= 15 else 1
)

print("WEIGHTED MODEL TRAINING")
print("-----------------------")
print("Training records:", len(X_train))
print("Testing records:", len(X_test))
print("Normal rainfall weight: 1")
print("Heavy rainfall weight: 3")
print("Heavy rainfall training records:", int((y_train >= 15).sum()))

# Create Random Forest model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

# Train using sample weights
print("\nTraining weighted Random Forest...")
model.fit(
    X_train,
    y_train,
    sample_weight=sample_weights
)

# Predict rainfall
predictions = model.predict(X_test)

# Overall evaluation
print("\nOVERALL MODEL PERFORMANCE")
print("--------------------------")
print("MAE:", round(mean_absolute_error(y_test, predictions), 3))
print("RMSE:", round(mean_squared_error(y_test, predictions) ** 0.5, 3))
print("R2:", round(r2_score(y_test, predictions), 3))

# Evaluate heavy rainfall
heavy_mask = y_test >= 15

actual_heavy = y_test[heavy_mask]
predicted_heavy = predictions[heavy_mask]

print("\nHEAVY RAINFALL PERFORMANCE")
print("--------------------------")
print("Heavy rainfall records:", len(actual_heavy))
print("Average actual rainfall:", round(actual_heavy.mean(), 2), "mm")
print("Average predicted rainfall:", round(predicted_heavy.mean(), 2), "mm")
print(
    "Average prediction error:",
    round((predicted_heavy - actual_heavy).mean(), 2),
    "mm"
)

print(
    "Underpredicted records:",
    int((predicted_heavy > predicted_heavy * 0 + actual_heavy).sum())
    if False else int((predicted_heavy < actual_heavy).sum())
)

print(
    "Predictions below half actual:",
    int((predicted_heavy < actual_heavy * 0.5).sum())
)

# Evaluate each rainfall category
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
        error = mean_absolute_error(
            y_test[mask],
            predictions[mask]
        )

        print(
            category,
            "| Records:", int(mask.sum()),
            "| MAE:", round(error, 3), "mm"
        )

# Save predictions separately
test_df = df.loc[test_mask].copy()
test_df["Predicted_Rainfall"] = predictions

test_df.to_csv(
    "data/weighted_weather_model_predictions.csv",
    index=False
)

# Save experimental model separately
joblib.dump(
    {
        "model": model,
        "feature_columns": X.columns.tolist()
    },
    "weighted_weather_prediction_model.pkl"
)

print("\nWeighted model saved successfully!")
print("File: weighted_weather_prediction_model.pkl")
print("Predictions: data/weighted_weather_model_predictions.csv")
