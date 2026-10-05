import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

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

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Model Training Completed")
print("Accuracy:", accuracy)

with open("fake_website_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model saved as fake_website_model.pkl")