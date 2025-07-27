import network
import time
import dht
import urequests
from machine import Pin, I2C
import ssd1306

# Config WiFi
SSID = 'Agua-de-oro'
PASSWORD = 'Dior5107'

# URL del backend Flask
FLASK_URL = 'http://192.168.0.181:5000/datos'

# Inicializar sensor DHT11 (GPIO 15)
sensor = dht.DHT11(Pin(15))

# Inicializar pantalla OLED
i2c = I2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def mostrar_en_pantalla(temp, hum):
    oled.fill(0)  # Borrar pantalla
    oled.text("Sensor DHT11", 0, 0)
    oled.text("Temp: {} C".format(temp), 0, 20)
    oled.text("Hum: {} %".format(hum), 0, 35)
    oled.show()

# Inicializar LEDs
led_verde = Pin(18, Pin.OUT)     # LED verde: sistema encendido
led_amarillo = Pin(26, Pin.OUT)  # LED amarillo: temperatura disminuye
led_rojo = Pin(19, Pin.OUT)      # LED rojo: temperatura aumenta

# Encender LED verde (indicador de funcionamiento)
led_verde.on()

# Guardar última temperatura para comparación
temp_anterior = None

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando al WiFi...')
        wlan.connect(SSID, PASSWORD)
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
    if wlan.isconnected():
        print('✅ Conectado al WiFi:', wlan.ifconfig()[0])
    else:
        print('❌ No se pudo conectar al WiFi')

# Bucle principal
conectar_wifi()
while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        print("🌡️ Temp:", temp, "°C | 💧 Hum:", hum, "%")

        # Mostrar en pantalla OLED
        mostrar_en_pantalla(temp, hum)

        # Control de LEDs según temperatura
        if temp_anterior is not None:
            if temp > temp_anterior:
                led_rojo.on()
                led_amarillo.off()
            elif temp < temp_anterior:
                led_rojo.off()
                led_amarillo.on()
            else:
                led_rojo.off()
                led_amarillo.off()
        else:
            led_rojo.off()
            led_amarillo.off()

        temp_anterior = temp

        # Enviar al servidor
        datos = {'temperatura': temp, 'humedad': hum}
        respuesta = urequests.post(FLASK_URL, json=datos)
        print("📡 Respuesta del servidor:", respuesta.text)
        respuesta.close()

    except Exception as e:
        print("❌ Error:", e)

    time.sleep(10)  # Esperar 10 segundos (modificable)
