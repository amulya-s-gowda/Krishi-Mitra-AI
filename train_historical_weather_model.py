
import pickle
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# --------------------------------------------------
# 1. CONFIGURATION
# --------------------------------------------------

DATA_FILE = "data/historical_weather_prediction_dataset.csv"

MODEL_FILE = "historical_weather_prediction_model.pkl"

PREDICTIONS_FILE = "data/historical_weather_model_predictions.csv"

FEATURES = [
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

TARGET = "Next_Day_Rainfall"


# --------------------------------------------------
# 2. LOAD DATA
# --------------------------------------------------

df = pd.read_csv(DATA_FILE, parse_dates=["Date"])

df = df.sort_values("Date").reset_index(drop=True)

# One-hot encode districts.
# The same columns are retained for every time period.
X = pd.get_dummies(
    df[FEATURES],
    columns=["District"],
    dtype=int
)

y = df[TARGET]

train_mask = df["Date"].dt.year <= 2023
validation_mask = df["Date"].dt.year == 2024
test_mask = df["Date"].dt.year == 2025

X_train = X.loc[train_mask]
y_train = y.loc[train_mask]

X_val = X.loc[validation_mask]
y_val = y.loc[validation_mask]

X_test = X.loc[test_mask]
y_test = y.loc[test_mask]

print("\nHISTORICAL DATA SPLITTING")
print("--------------------------------")
print("Training records:", len(X_train))
print("Validation records:", len(X_val))
print("Testing records:", len(X_test))
print("Features:", X.shape[1])


# --------------------------------------------------
# 3. EVALUATION FUNCTION
# --------------------------------------------------

def evaluate(name, actual, predicted):

    mae = mean_absolute_error(actual, predicted)

    rmse = np.sqrt(
        mean_squared_error(actual, predicted)
    )

    r2 = r2_score(actual, predicted)

    print(
        f"{name:<28} "
        f"MAE: {mae:.3f} | "
        f"RMSE: {rmse:.3f} | "
        f"R2: {r2:.3f}"
    )

    return {
        "Model": name,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    }


# --------------------------------------------------
# 4. VALIDATION BASELINES
# --------------------------------------------------

print("\nVALIDATION BASELINES")
print("--------------------------------")

validation_results = []

validation_results.append(
    evaluate(
        "Zero rainfall baseline",
        y_val,
        np.zeros(len(y_val))
    )
)

validation_results.append(
    evaluate(
        "Persistence baseline",
        y_val,
        df.loc[validation_mask, "PRECTOTCORR"]
    )
)


# --------------------------------------------------
# 5. COMPARE RANDOM FOREST CONFIGURATIONS
# --------------------------------------------------

candidates = [
    {
        "n_estimators": 100,
        "min_samples_leaf": 1
    },
    {
        "n_estimators": 150,
        "min_samples_leaf": 2
    },
    {
        "n_estimators": 200,
        "min_samples_leaf": 3
    }
]

best_model = None
best_params = None
best_mae = float("inf")

print("\nRANDOM FOREST VALIDATION")
print("--------------------------------")

for params in candidates:

    model = RandomForestRegressor(
        n_estimators=params["n_estimators"],
        min_samples_leaf=params["min_samples_leaf"],
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    val_predictions = model.predict(X_val)

    result = evaluate(
        f"RF {params}",
        y_val,
        val_predictions
    )

    validation_results.append(result)

    # Select using validation MAE only
    if result["MAE"] < best_mae:

        best_mae = result["MAE"]
        best_model = model
        best_params = params


print("\nSELECTED MODEL")
print("--------------------------------")
print("Parameters:", best_params)
print("Validation MAE:", round(best_mae, 3))


# --------------------------------------------------
# 6. FINAL TRAINING ON 2013-2024
# --------------------------------------------------

print("\nTRAINING FINAL MODEL")
print("--------------------------------")

final_train_mask = df["Date"].dt.year <= 2024

X_final_train = X.loc[final_train_mask]
y_final_train = y.loc[final_train_mask]

final_model = RandomForestRegressor(
    n_estimators=best_params["n_estimators"],
    min_samples_leaf=best_params["min_samples_leaf"],
    random_state=42,
    n_jobs=-1
)

final_model.fit(
    X_final_train,
    y_final_train
)


# --------------------------------------------------
# 7. FINAL TEST ON 2025
# --------------------------------------------------

print("\nFINAL TEST RESULTS - 2025")
print("--------------------------------")

test_predictions = final_model.predict(X_test)

test_predictions = np.maximum(
    test_predictions,
    0
)

test_results = []

test_results.append(
    evaluate(
        "Historical Random Forest",
        y_test,
        test_predictions
    )
)

test_results.append(
    evaluate(
        "Zero rainfall baseline",
        y_test,
        np.zeros(len(y_test))
    )
)

test_results.append(
    evaluate(
        "Persistence baseline",
        y_test,
        df.loc[test_mask, "PRECTOTCORR"]
    )
)


# --------------------------------------------------
# 8. SAVE PREDICTIONS
# --------------------------------------------------

predictions_df = df.loc[
    test_mask,
    ["Date", "District", TARGET]
].copy()

predictions_df["Predicted_Rainfall"] = test_predictions

predictions_df["Absolute_Error"] = abs(
    predictions_df[TARGET] -
    predictions_df["Predicted_Rainfall"]
)

predictions_df.to_csv(
    PREDICTIONS_FILE,
    index=False
)


# --------------------------------------------------
# 9. SAVE FINAL MODEL
# --------------------------------------------------

model_package = {
    "model": final_model,
    "feature_columns": X.columns.tolist(),
    "features": FEATURES,
    "best_parameters": best_params,
    "training_period": "2013-2024",
    "testing_period": "2025"
}

with open(MODEL_FILE, "wb") as file:
    pickle.dump(model_package, file)


# --------------------------------------------------
# 10. FEATURE IMPORTANCE
# --------------------------------------------------

importance = pd.Series(
    final_model.feature_importances_,
    index=X.columns
).sort_values(ascending=False)

print("\nTOP 10 IMPORTANT FEATURES")
print("--------------------------------")
print(importance.head(10).to_string())

importance.to_csv(
    "data/historical_feature_importance.csv",
    header=["Importance"]
)


# --------------------------------------------------
# 11. SAVE METRICS
# --------------------------------------------------

pd.DataFrame(
    validation_results
).to_csv(
    "data/historical_validation_metrics.csv",
    index=False
)

pd.DataFrame(
    test_results
).to_csv(
    "data/historical_test_metrics.csv",
    index=False
)


print("\nHISTORICAL MODEL TRAINING COMPLETED")
print("--------------------------------")
print("Model:", MODEL_FILE)
print("Predictions:", PREDICTIONS_FILE)
print("Validation metrics: data/historical_validation_metrics.csv")
print("Test metrics: data/historical_test_metrics.csv")
print("Feature importance: data/historical_feature_importance.csv")
