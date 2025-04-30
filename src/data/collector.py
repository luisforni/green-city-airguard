import csv
import os
import time
from src.sensors.read_sensors import read_all

OUTPUT_FILE = "data/dataset.csv"
INTERVAL_SECONDS = 60  # recolectar cada 1 minuto

# Cabecera del CSV
HEADERS = [
    "timestamp", "temperature", "humidity", "air_quality", "pm1_0", "pm2_5", "pm10"
]

def init_csv():
    if not os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, mode='w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writeheader()

def append_data():
    data = read_all()
    with open(OUTPUT_FILE, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writerow(data)

def main():
    init_csv()
    print("Recolectando datos cada", INTERVAL_SECONDS, "segundos. Presiona Ctrl+C para salir.")
    try:
        while True:
            append_data()
            time.sleep(INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\nFinalizado.")

if __name__ == "__main__":
    main()
