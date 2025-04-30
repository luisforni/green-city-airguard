import joblib
from src.sensors.read_sensors import read_all
import time

MODEL_PATH = "src/model/air_quality_model.pkl"

# Cargar el modelo entrenado
model = joblib.load(MODEL_PATH)

print("Modelo de calidad del aire cargado. Iniciando predicciones en tiempo real...")

try:
    while True:
        data = read_all()
        if None in [
            data["temperature"],
            data["humidity"],
            data["air_quality"],
            data["pm1_0"],
            data["pm2_5"],
            data["pm10"]
        ]:
            print("Lectura incompleta, intentando de nuevo...")
            time.sleep(5)
            continue

        features = [[
            data["temperature"],
            data["humidity"],
            data["air_quality"],
            data["pm1_0"],
            data["pm2_5"],
            data["pm10"]
        ]]
        prediction = model.predict(features)[0]

        print(f"{data['timestamp']} | Calidad del aire: {prediction.upper()}")
        time.sleep(60)  # cada minuto

except KeyboardInterrupt:
    print("\nPredicción finalizada.")
