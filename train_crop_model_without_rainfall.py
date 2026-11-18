
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    cross_val_score
)
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
df = pd.read_csv("data/Crop_recommendation.csv")

# Use six features, excluding rainfall
features = [
    "N", "P", "K",
    "temperature", "humidity", "ph"
]

X = df[features]
y = df["label"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Train experimental model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)
# Save experimental model separately
saved_data = {
    "model": model,
    "feature_columns": features
}

joblib.dump(
    saved_data,
    "crop_recommendation_model_no_rainfall.pkl"
)

print("\nExperimental model saved successfully!")

# Test accuracy
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\nCROP MODEL WITHOUT RAINFALL")
print("---------------------------")

print("Training records:", len(X_train))
print("Testing records:", len(X_test))
print("Accuracy:", round(accuracy * 100, 2), "%")

print("\nCLASSIFICATION REPORT")
print(classification_report(y_test, predictions))

# Five-fold cross-validation
cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

scores = cross_val_score(
    model,
    X,
    y,
    cv=cv,
    scoring="accuracy"
)

print("\n5-FOLD CROSS VALIDATION")
print("Individual scores:", scores.round(4))
print("Average accuracy:", round(scores.mean() * 100, 2), "%")
