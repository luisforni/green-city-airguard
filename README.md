# 🌿 GreenCity AirGuard – IoT Ambiental con ML

Sistema completo basado en **Raspberry Pi 4** que mide condiciones ambientales, predice en tiempo real la **calidad del aire** y el **riesgo de incendio**, y los visualiza en un dashboard local o web. Ideal para proyectos de sostenibilidad, Smart Cities y monitoreo distribuido.

---

## 🧰 Hardware necesario

- **Raspberry Pi 4** (2 GB RAM o más)
- **Sensor DHT22** – Temperatura y humedad (digital)
- **Sensor MQ135** – Calidad del aire (requiere ADC)
- **Sensor PMS5003** – PM1.0, PM2.5, PM10 (UART)
- **MCP3008** – Conversor ADC (para MQ135)
- Protoboard, cables dupont
- Resistencia 10kΩ para el DHT22

---

## ⚡ Conexiones físicas

### DHT22 (temperatura y humedad)
- VCC → 3.3V (Pin 1)
- GND → GND (Pin 6)
- DATA → GPIO 4 (Pin 7)
- Conectar resistencia 10kΩ entre VCC y DATA

### MQ135 (requiere MCP3008 ADC)
- MQ135 AO → MCP3008 CH0
- MCP3008:
  - VDD, VREF → 3.3V (Pin 1)
  - AGND, DGND → GND (Pin 6)
  - CLK → GPIO 11 (Pin 23)
  - DOUT → GPIO 9 (Pin 21)
  - DIN → GPIO 10 (Pin 19)
  - CS → GPIO 8 (Pin 24)

### PMS5003 (UART)
- VCC → 5V (Pin 2)
- GND → GND (Pin 6)
- TXD → GPIO 15 (Pin 10)
- RXD → GPIO 14 (Pin 8)

> Nota: activa la interfaz **SPI** y **UART** con:
```bash
sudo raspi-config
# Interfacing Options → SPI → Enable
# Interfacing Options → Serial → Disable login shell, enable hardware UART
```

---

## ⚙️ Instalación y configuración

### 1. Clona el repositorio
```bash
git clone https://github.com/luisforni/green-city-airguard.git
cd green-city-airguard
```

### 2. Instala las dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecuta la recolección de datos (opcional)
```bash
python src/data/collector.py
```

### 4. Entrena los modelos
```bash
python src/model/train_model.py     # Modelo calidad del aire
python src/model/train_fire_model.py  # (opcional) riesgo de incendio
```

### 5. Ejecuta las predicciones
```bash
python src/model/predict_air_quality.py
python src/model/predict.py
```

### 6. Dashboard local (modo kiosco)
```bash
python src/dashboard/local_dashboard.py
```

### 7. Dashboard web (modo servidor)
```bash
python src/dashboard/server_dashboard.py
```
Luego accede desde otro dispositivo:
```
http://IP-DE-LA-RASPBERRY:8501
```

---

## 🖥️ Modo kiosco automático (opcional)
Puedes configurar tu Raspberry Pi para que arranque directamente en el dashboard. Consulta la **Guía de despliegue**.

---

## 📂 Estructura del proyecto
```
green-city-airguard/
├── data/
│   └── dataset.csv
├── src/
│   ├── data/
│   │   └── collector.py
│   ├── dashboard/
│   │   ├── local_dashboard.py
│   │   └── server_dashboard.py
│   ├── model/
│   │   ├── train_model.py
│   │   ├── train_fire_model.py
│   │   ├── predict_air_quality.py
│   │   └── predict.py
│   └── sensors/
│       ├── read_sensors.py
│       └── read_pms5003.py
└── requirements.txt
```

---

## 🧠 Créditos
Desarrollado por [Luis Forni](https://www.linkedin.com/in/luis-forni-97aa49223) | forni.luis@gmail.com

---

## 🪪 Licencia
MIT – puedes usarlo, mejorarlo y compartirlo libremente. Créditos bienvenidos.
