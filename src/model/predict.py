import joblib
from src.sensors.read_sensors import read_all
import time

MODEL_PATH = "src/model/fire_risk_model.pkl"

# Cargar el modelo entrenado
model = joblib.load(MODEL_PATH)

print("Modelo de riesgo de incendio cargado. Iniciando predicciones en tiempo real...")

try:
    while True:
        data = read_all()
        if None in [data["temperature"], data["humidity"], data["air_quality"]]:
            print("Lectura incompleta, intentando de nuevo...")
            time.sleep(5)
            continue

        features = [[
            data["temperature"],
            data["humidity"],
            data["air_quality"]
        ]]
        prediction = model.predict(features)[0]

        print(f"{data['timestamp']} | Riesgo de incendio: {prediction.upper()}")
        time.sleep(60)

except KeyboardInterrupt:
    print("\nPredicción finalizada.")
