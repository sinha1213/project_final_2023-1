from time import sleep
import json

import paho.mqtt.client as mqtt
from gpiozero import LED
import adafruit_dht
import board

dht_device = adafruit_dht.DHT22(board.D4)

password123 = 12345

def get_data():
    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            # password123 = initial_password
            return temperature, humidity, password123
        except RuntimeError as error:
            sleep(2.0)
            continue

MY_ID = "05"

MQTT_HOST = "mqtt-dashboard.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_SUB_TOPIC = f"mobile/{MY_ID}/light"
MQTT_SUB_ALL_TOPIC = f"mobile/all/light"
MQTT_PUB_TOPIC = f"mobile/{MY_ID}/sensing"

led = LED(23)
#####################################
import board
import neopixel

pixel_pin = board.D10
num_pixels = 4
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness = 0.7, auto_write=False, pixel_order=neopixel.GRB)
#######################################

def on_message(client, userdata, message):
    result = str(message.payload.decode("utf-8"))
    value = json.loads(result)
    action = value['action']
    print(f"action = {action}")
    if action.upper() == "WELCOME":
        print("Welcome")
        pixels[0] = (255,255,255)
        pixels[1] = (255,255,255)
        pixels[2] = (255,255,255)
        pixels[3] = (255,255,255)
        pixels.show()

    elif action.upper() == "BYE":
        print("You are not allow to come in")
        pixels[0] = (255,0,0)
        pixels[1] = (1,0,255)
        pixels[2] = (255,0,0)
        pixels[3] = (1,0,255)
        pixels.show()

    else:
        print("Illegal Argument Exception!")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
client.subscribe(MQTT_SUB_TOPIC)
client.subscribe(MQTT_SUB_ALL_TOPIC)
client.loop_start()

try:
    while True :
        temperature, humidity, password123 = get_data()
        sensing = {
            "temperature" : temperature,
            "humidity" : humidity, 
            "password123" : password123
        }
        value = json.dumps(sensing)
        client.publish(MQTT_PUB_TOPIC, value)
        print(value)

        sleep(1)
except KeyboardInterrupt:
    print("종료합니다!!")
finally:
    client.loop_stop()
    client.disconnect()

