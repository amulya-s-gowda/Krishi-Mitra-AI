
import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load prepared dataset
df = pd.read_csv("data/weather_prediction_dataset.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Define features (must match training)
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

# Prepare testing data
test_mask = df["Date"].dt.year == 2025
test_df = df.loc[test_mask].copy()

X_test = pd.get_dummies(
    test_df[features],
    columns=["District"],
    dtype=int
)

# Load trained model
saved_model = joblib.load("weather_prediction_model.pkl")

model = saved_model["model"]
feature_columns = saved_model["feature_columns"]

# Ensure columns match the training dataset
X_test = X_test.reindex(
    columns=feature_columns,
    fill_value=0
)

y_actual = test_df["Next_Day_Rainfall"]
y_predicted = model.predict(X_test)

# Save predictions
test_df["Predicted_Rainfall"] = y_predicted
test_df["Absolute_Error"] = abs(
    y_actual - y_predicted
)

test_df.to_csv(
    "data/weather_model_predictions.csv",
    index=False
)

# Overall evaluation
print("\nOVERALL MODEL PERFORMANCE")
print("-------------------------")
print("MAE:", round(mean_absolute_error(y_actual, y_predicted), 3))
print("RMSE:", round(mean_squared_error(y_actual, y_predicted) ** 0.5, 3))
print("R2:", round(r2_score(y_actual, y_predicted), 3))

# Rainfall category evaluation
# Categories are descriptive thresholds for analysis,
# not official IMD rainfall classifications.
conditions = [
    y_actual < 0.1,
    (y_actual >= 0.1) & (y_actual < 2.5),
    (y_actual >= 2.5) & (y_actual < 15),
    y_actual >= 15
]

categories = [
    "No rain",
    "Very light rain",
    "Light to moderate rain",
    "Heavier rain"
]

test_df["Actual_Category"] = pd.Series(
    pd.cut(
        y_actual,
        bins=[-0.001, 0.1, 2.5, 15, float("inf")],
        labels=categories,
        right=False
    ),
    index=test_df.index
)

print("\nERROR BY ACTUAL RAINFALL CATEGORY")
print("---------------------------------")

for category in categories:
    mask = test_df["Actual_Category"] == category

    if mask.sum() > 0:
        category_error = mean_absolute_error(
            y_actual[mask],
            y_predicted[mask]
        )

        print(
            category,
            "| Records:", int(mask.sum()),
            "| MAE:", round(category_error, 3), "mm"
        )

# Feature importance
importance = pd.Series(
    model.feature_importances_,
    index=feature_columns
).sort_values(ascending=False)

print("\nTOP 10 IMPORTANT FEATURES")
print("-------------------------")
print(importance.head(10))

# Plot actual vs predicted rainfall sample
plt.figure(figsize=(8, 6))

sample_size = min(1000, len(y_actual))

plt.scatter(
    y_actual.iloc[:sample_size],
    y_predicted[:sample_size],
    alpha=0.4
)

plt.xlabel("Actual Rainfall (mm)")
plt.ylabel("Predicted Rainfall (mm)")
plt.title("Actual vs Predicted Rainfall")
plt.tight_layout()

plt.savefig("data/actual_vs_predicted.png")
plt.show()

# Plot feature importance
plt.figure(figsize=(10, 6))

importance.head(10).sort_values().plot(kind="barh")

plt.title("Top 10 Important Weather Features")
plt.xlabel("Feature Importance")
plt.tight_layout()

plt.savefig("data/feature_importance.png")
plt.show()

print("\nEvaluation completed successfully!")
