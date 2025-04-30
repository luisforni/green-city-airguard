import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

DATASET_PATH = "data/dataset.csv"
MODEL_PATH = "src/model/fire_risk_model.pkl"

# Etiquetar el riesgo de incendio basado en humedad y temperatura
def assign_fire_risk(row):
    if row["temperature"] >= 30 and row["humidity"] <= 30:
        return "alto"
    elif row["temperature"] >= 25 and row["humidity"] <= 50:
        return "medio"
    else:
        return "bajo"

def main():
    df = pd.read_csv(DATASET_PATH)
    df = df.dropna()

    df["fire_risk_level"] = df.apply(assign_fire_risk, axis=1)

    X = df[["temperature", "humidity", "air_quality"]]
    y = df["fire_risk_level"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(clf, MODEL_PATH)
    print(f"Modelo guardado en {MODEL_PATH}")

if __name__ == "__main__":
    main()
