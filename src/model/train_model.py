import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

DATASET_PATH = "data/dataset.csv"
MODEL_PATH = "src/model/air_quality_model.pkl"

# Nueva asignación de categorías de calidad del aire
def assign_air_quality(row):
    if row["pm2_5"] is None or row["pm10"] is None:
        return "desconocida"
    elif row["pm2_5"] <= 12 and row["pm10"] <= 50:
        return "buena"
    elif row["pm2_5"] <= 35 and row["pm10"] <= 100:
        return "moderada"
    else:
        return "mala"

def main():
    df = pd.read_csv(DATASET_PATH)
    df = df.dropna()

    # Etiquetar datos con niveles de calidad del aire
    df["air_quality_level"] = df.apply(assign_air_quality, axis=1)

    X = df[["temperature", "humidity", "air_quality", "pm1_0", "pm2_5", "pm10"]]
    y = df["air_quality_level"]

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
