import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

data = pd.read_csv("website_data.csv")

features = [
    "https",
    "ip_address",
    "url_length",
    "at_symbol",
    "hyphen",
    "dots",
    "suspicious_words"
]

X = data[features]
y = data["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

with open("fake_website_model.pkl", "rb") as file:
    model = pickle.load(file)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\n===== MODEL EVALUATION =====")

print("\nAccuracy:")
print(accuracy)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

print("\nClassification Report:")
print(classification_report(
    y_test,
    predictions,
    target_names=["Safe", "Fake/Suspicious"]
))