
import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load crop dataset
df = pd.read_csv("data/Crop_recommendation.csv")

# Separate input features and target crop
X = df.drop("label", axis=1)
y = df["label"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training records:", len(X_train))
print("Testing records:", len(X_test))

# Create Random Forest classifier
crop_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train the model
print("\nTraining crop recommendation model...")
crop_model.fit(X_train, y_train)

# Make predictions
y_pred = crop_model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)

print("\nCROP MODEL EVALUATION")
print("---------------------")
print("Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save trained model and feature names
model_data = {
    "model": crop_model,
    "feature_columns": list(X.columns)
}

with open("crop_recommendation_model.pkl", "wb") as file:
    pickle.dump(model_data, file)

print("\nCrop model trained successfully!")
print("Saved as: crop_recommendation_model.pkl")
