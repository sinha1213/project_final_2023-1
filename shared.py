# from time import sleep
# import json
# import paho.mqtt.client as mqtt
# import adafruit_dht
# import board

# # Initialize the DHT22 sensor
# dht_device = adafruit_dht.DHT22(board.D4)

# def get_data():
#     while True:
#         try:
#             temperature = dht_device.temperature
#             humidity = dht_device.humidity
#             return temperature, humidity
#         except RuntimeError as error:
#             sleep(2.0)
#             continue

# # MQTT settings
# MY_ID = "05"
# MQTT_HOST = "mqtt-dashboard.com"
# MQTT_PORT = 1883
# MQTT_KEEPALIVE_INTERVAL = 60
# MQTT_PUB_TOPIC = f"mobile/{MY_ID}/sensing"

# # Initialize MQTT client
# client = mqtt.Client()

# # Connect to MQTT broker
# client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
# client.loop_start()

# try:
#     while True:
#         temperature, humidity = get_data()
#         sensing = {
#             "temperature": temperature,
#             "humidity": humidity
#         }
#         value = json.dumps(sensing)
#         client.publish(MQTT_PUB_TOPIC, value)
#         sleep(0.5)
# except KeyboardInterrupt:
#     pass
# finally:
#     client.loop_stop()
#     client.disconnect()
















# from time import sleep
# import json
# import paho.mqtt.client as mqtt
# import adafruit_dht
# import board

# # Initialize the DHT22 sensor
# dht_device = adafruit_dht.DHT22(board.D4)

# def get_data():
#     while True:
#         try:
#             temperature = dht_device.temperature
#             humidity = dht_device.humidity
#             return temperature, humidity
#         except RuntimeError as error:
#             sleep(2.0)
#             continue

# # MQTT settings
# MY_ID = "05"
# MQTT_HOST = "mqtt-dashboard.com"
# MQTT_PORT = 1883
# MQTT_KEEPALIVE_INTERVAL = 60
# MQTT_PUB_TOPIC = f"mobile/{MY_ID}/sensing"

# # Initialize MQTT client
# client = mqtt.Client()

# # Connect to MQTT broker
# client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
# client.loop_start()

# try:
#     while True:
#         temperature, humidity = get_data()
#         sensing = {
#             "temperature": temperature,
#             "humidity": humidity
#         }
#         value = json.dumps(sensing)
#         client.publish(MQTT_PUB_TOPIC, value)
#         sleep(0.5)
# except KeyboardInterrupt:
#     pass
# finally:
#     client.loop_stop()
#     client.disconnect()






from time import sleep
import json
import paho.mqtt.client as mqtt
import adafruit_dht
import board

dht_device = adafruit_dht.DHT22(board.D4)

def get_data():
    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            return temperature, humidity
        except RuntimeError as error:
            sleep(2.0)
            continue

MY_ID = "05"

MQTT_HOST = "mqtt-dashboard.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_PUB_TOPIC = f"mobile/{MY_ID}/sensing"

client = mqtt.Client()
client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
client.loop_start()

try:
    while True:
        temperature, humidity = get_data()
        sensing = {
            "temperature": temperature,
            "humidity": humidity
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
