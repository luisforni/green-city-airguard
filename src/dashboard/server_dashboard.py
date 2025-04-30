import flet as ft
import joblib
import time
from src.sensors.read_sensors import read_all

# Cargar modelos
fire_model = joblib.load("src/model/fire_risk_model.pkl")
air_model = joblib.load("src/model/air_quality_model.pkl")

def main(page: ft.Page):
    page.title = "GreenCity IoT - Monitoreo Web"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    title = ft.Text("GreenCity IoT - Dashboard Web", size=24, weight="bold")
    temperature_text = ft.Text()
    humidity_text = ft.Text()
    air_quality_sensor_text = ft.Text()
    pm_text = ft.Text()
    fire_risk_text = ft.Text(size=22, weight="bold")
    air_quality_pred_text = ft.Text(size=22, weight="bold")

    def update_dashboard():
        while True:
            data = read_all()
            if None in [data["temperature"], data["humidity"], data["air_quality"], data["pm1_0"], data["pm2_5"], data["pm10"]]:
                fire_risk_text.value = "Lectura incompleta"
                air_quality_pred_text.value = "Lectura incompleta"
                page.update()
                time.sleep(5)
                continue

            # Predicciones
            fire_features = [[data["temperature"], data["humidity"], data["air_quality"]]]
            air_features = [[data["temperature"], data["humidity"], data["air_quality"], data["pm1_0"], data["pm2_5"], data["pm10"]]]

            fire_prediction = fire_model.predict(fire_features)[0]
            air_prediction = air_model.predict(air_features)[0]

            # Mostrar mediciones
            temperature_text.value = f"Temperatura: {data['temperature']} °C"
            humidity_text.value = f"Humedad: {data['humidity']} %"
            air_quality_sensor_text.value = f"Calidad del aire MQ135: {data['air_quality']} %"
            pm_text.value = f"PM2.5: {data['pm2_5']} µg/m³ | PM10: {data['pm10']} µg/m³"

            # Riesgo de incendio
            if fire_prediction == "alto":
                fire_risk_text.value = "RIESGO DE INCENDIO: ALTO"
                fire_risk_text.color = ft.colors.RED
            elif fire_prediction == "medio":
                fire_risk_text.value = "RIESGO DE INCENDIO: MEDIO"
                fire_risk_text.color = ft.colors.ORANGE
            else:
                fire_risk_text.value = "RIESGO DE INCENDIO: BAJO"
                fire_risk_text.color = ft.colors.GREEN

            # Calidad del aire
            if air_prediction == "mala":
                air_quality_pred_text.value = "CALIDAD DEL AIRE: MALA"
                air_quality_pred_text.color = ft.colors.RED
            elif air_prediction == "moderada":
                air_quality_pred_text.value = "CALIDAD DEL AIRE: MODERADA"
                air_quality_pred_text.color = ft.colors.ORANGE
            else:
                air_quality_pred_text.value = "CALIDAD DEL AIRE: BUENA"
                air_quality_pred_text.color = ft.colors.GREEN

            page.update()
            time.sleep(60)

    page.add(title, temperature_text, humidity_text, air_quality_sensor_text, pm_text, fire_risk_text, air_quality_pred_text)

    import threading
    threading.Thread(target=update_dashboard, daemon=True).start()

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8501)
