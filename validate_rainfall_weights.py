
import pandas as pd

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

# Convert district names into numerical columns
X = pd.get_dummies(
    df[features],
    columns=["District"],
    dtype=int
)

y = df[target]

# Split: 2023 for training, 2024 for validation
train_mask = df["Date"].dt.year == 2023
validation_mask = df["Date"].dt.year == 2024

X_train = X.loc[train_mask]
X_validation = X.loc[validation_mask]

y_train = y.loc[train_mask]
y_validation = y.loc[validation_mask]

print("RAINFALL WEIGHT VALIDATION")
print("--------------------------")
print("Training records:", len(X_train))
print("Validation records:", len(X_validation))

# Heavy rainfall threshold
HEAVY_RAINFALL_THRESHOLD = 15

# Try different heavy-rainfall weights
weights_to_test = [1, 2, 3, 4]

results = []

for weight in weights_to_test:

    print(f"\nTesting heavy rainfall weight: {weight}")

    # Assign sample weights
    sample_weights = y_train.apply(
        lambda rainfall: weight
        if rainfall >= HEAVY_RAINFALL_THRESHOLD
        else 1
    )

    # Create model
    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )

    # Train model
    model.fit(
        X_train,
        y_train,
        sample_weight=sample_weights
    )

    # Predict validation rainfall
    predictions = model.predict(X_validation)

    # Overall metrics
    overall_mae = mean_absolute_error(
        y_validation,
        predictions
    )

    overall_rmse = mean_squared_error(
        y_validation,
        predictions
    ) ** 0.5

    overall_r2 = r2_score(
        y_validation,
        predictions
    )

    # Heavy rainfall metrics
    heavy_mask = y_validation >= HEAVY_RAINFALL_THRESHOLD

    actual_heavy = y_validation[heavy_mask]
    predicted_heavy = predictions[heavy_mask]

    heavy_mae = mean_absolute_error(
        actual_heavy,
        predicted_heavy
    )

    heavy_error = (
        predicted_heavy - actual_heavy
    ).mean()

    underpredicted = (
        predicted_heavy < actual_heavy
    ).sum()

    below_half = (
        predicted_heavy < actual_heavy * 0.5
    ).sum()

    results.append({
        "Weight": weight,
        "Overall_MAE": overall_mae,
        "Overall_RMSE": overall_rmse,
        "Overall_R2": overall_r2,
        "Heavy_MAE": heavy_mae,
        "Heavy_Average_Error": heavy_error,
        "Heavy_Underpredictions": int(underpredicted),
        "Below_Half_Actual": int(below_half)
    })

# Display comparison
results_df = pd.DataFrame(results)

print("\n\nWEIGHT COMPARISON RESULTS")
print("-------------------------")

print(
    results_df.round(3).to_string(index=False)
)

# Save validation results
results_df.to_csv(
    "data/rainfall_weight_validation.csv",
    index=False
)

print("\nValidation results saved:")
print("data/rainfall_weight_validation.csv")
