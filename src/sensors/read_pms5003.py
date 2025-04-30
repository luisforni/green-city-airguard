import serial
import struct

# Configuración del puerto UART
UART_PORT = "/dev/serial0"  # Alias de GPIO14/15 en Raspberry Pi
BAUD_RATE = 9600

# Iniciar la conexión serial
ser = serial.Serial(UART_PORT, BAUD_RATE, timeout=2)

def read_pms5003():
    header = ser.read(2)
    if header != b'\x42\x4d':
        return None  # No es un paquete válido

    frame = ser.read(30)
    if len(frame) != 30:
        return None

    data = struct.unpack(
        '>HHHHHHHHHHHHHH', frame[:28]
    )

    pm1_0_cf1 = data[0]
    pm2_5_cf1 = data[1]
    pm10_cf1 = data[2]

    pm1_0_atm = data[3]
    pm2_5_atm = data[4]
    pm10_atm = data[5]

    return {
        "pm1_0": pm1_0_atm,
        "pm2_5": pm2_5_atm,
        "pm10": pm10_atm
    }

if __name__ == "__main__":
    from time import sleep
    while True:
        result = read_pms5003()
        if result:
            print(result)
        else:
            print("Esperando datos válidos...")
        sleep(2)
