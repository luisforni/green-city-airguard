import Adafruit_DHT
from gpiozero import MCP3008
from datetime import datetime
from src.sensors.read_pms5003 import read_pms5003

# Configuración de pines
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4  # GPIO4 para el DHT22
MQ135_CHANNEL = 0  # Canal 0 del MCP3008 para el MQ135

# Inicializar el ADC
mq135 = MCP3008(channel=MQ135_CHANNEL)

def read_all():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    air_quality = mq135.value * 100  # valor entre 0-100%
    pms_data = read_pms5003() or {"pm1_0": None, "pm2_5": None, "pm10": None}

    data = {
        "timestamp": datetime.now().isoformat(),
        "temperature": round(temperature, 2) if temperature else None,
        "humidity": round(humidity, 2) if humidity else None,
        "air_quality": round(air_quality, 2),
        "pm1_0": pms_data["pm1_0"],
        "pm2_5": pms_data["pm2_5"],
        "pm10": pms_data["pm10"]
    }
    return data

if __name__ == "__main__":
    from time import sleep
    while True:
        print(read_all())
        sleep(5)
