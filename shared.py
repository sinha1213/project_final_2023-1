from time import sleep
import json
# import shared
import final1.py

import paho.mqtt.client as mqtt
from gpiozero import LED
import adafruit_dht
import board
import neopixel

# DHT22 센서 설정
dht_device = adafruit_dht.DHT22(board.D4)
# 초기 비밀번호 설정
password123 = int(final1.initial_password)
# password123 = 123

def get_data():
    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            password123 = int(final1.current_password)  # shared 모듈에서 현재 비밀번호를 가져옴
            # password123 = 123
            return temperature, humidity, password123
        except RuntimeError as error:
            sleep(2.0)
            continue

# MQTT 설정
MY_ID = "05"
MQTT_HOST = "mqtt-dashboard.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_SUB_TOPIC = f"mobile/{MY_ID}/light"
MQTT_SUB_ALL_TOPIC = f"mobile/{MY_ID}/light"
MQTT_PUB_TOPIC = f"mobile/{MY_ID}/sensing"

# LED 설정
led = LED(23)
pixel_pin = board.D10
num_pixels = 4
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.7, auto_write=False, pixel_order=neopixel.GRB)

# MQTT 메시지 처리 함수
def on_message(client, userdata, message):
    result = str(message.payload.decode("utf-8"))
    value = json.loads(result)
    action = value['action']
    if action.upper() == "WELCOME":
        pixels.fill((255, 255, 255))
        pixels.show()
    elif action.upper() == "BYE":
        pixels.fill((255, 0, 0))
        pixels.show()
    else:
        pass

# MQTT 클라이언트 설정 및 연결
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
client.subscribe(MQTT_SUB_TOPIC)
client.subscribe(MQTT_SUB_ALL_TOPIC)
client.loop_start()

try:
    while True:
        temperature, humidity, password123 = get_data()
        sensing = {
            "temperature": temperature,
            "humidity": humidity,
            "password123": password123
        }
        value = json.dumps(sensing)
        client.publish(MQTT_PUB_TOPIC, value)
        sleep(1)
except KeyboardInterrupt:
    pass
finally:
    client.loop_stop()
    client.disconnect()