import getpass
from time import sleep


## 초음파센서 ##
from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
factory = PiGPIOFactory()
sensor = DistanceSensor(echo=19, trigger=13, pin_factory=factory)
####################
### LED ###
from gpiozero import LED
led_R = LED(27)
led_G = LED(22)
led_Y = LED(23)
###############
### LED-strip ###
import board
import neopixel

pixel_pin = board.D10
num_pixels = 4
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness = 0.7, auto_write=False, pixel_order=neopixel.GRB)
#############
#### Buzzer ###
from gpiozero import PWMOutputDevice
buzzer_pin = 12
pwm_device = PWMOutputDevice(pin=buzzer_pin, frequency=0,initial_value=0.5)
tones = [0, 261, 294, 329, 349, 392, 440, 493, 523]
beep_music = [8, 1, 8, 1, 8, 1, 8, 1]
beep_term = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
welcome_music = [1, 3, 5, 8]
welcome_term = [1, 1, 1, 1]
Whereareyou_music = [8, 1, 0, 8, 1]
Whereareyou_term = [1, 0.5, 1, 1, 0.5]
##############
### Button ###
from gpiozero import Button
button = Button(24, pull_up=False, bounce_time = 0.1) #bounce_time = 0.1

def button_pressed():
    print("Where are you")
    for h in range(len(Whereareyou_music)):
        pwm_device.frequency = tones[Whereareyou_music[h]]
        pwm_device.value = 0.5 
        sleep(Whereareyou_term[h])
        pwm_device.value = 0
#button.when_pressed = button_pressed

###################
### moter ###
import RPi.GPIO as GPIO
import time

servo_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # 주파수 50Hz로 설정
pwm.start(0)

def set_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

set_angle(0)
######################

pixels[0] = (0,0,0)
pixels[1] = (0,0,0)
pixels[2] = (0,0,0)
pixels[3] = (0,0,0)
pixels.show()

while True:
    button.when_pressed = button_pressed
    print(round(sensor.distance * 100, 2))
    sleep(1.0)
    if (round(sensor.distance * 100, 2) <= 4.1):
        break

while True:
    button.when_pressed = button_pressed
    led_Y.on()
    initiation_password = getpass.getpass("초기 비밀번호: ")
    if initiation_password == '0000':
        print("Please change the password_ Do not use \"0000\".")
    else:
        led_Y.off()
        break

i = 0
while (i != 3):
    button.when_pressed = button_pressed
    led_G.on()
    current_password = getpass.getpass("Tell me a password: ")
    if (current_password == initiation_password):
        print("You Welcome")
        for k in range(5):
            led_G.off()
            sleep(0.3)
            led_G.on()
            sleep(0.3)
        pixels[0] = (255,255,255)
        pixels[1] = (255,255,255)
        pixels[2] = (255,255,255)
        pixels[3] = (255,255,255)
        pixels.show()
        for h in range(len(welcome_music)):
            pwm_device.frequency = tones[welcome_music[h]]
            pwm_device.value = 0.5  # 50% duty cycle
            sleep(welcome_term[h])
            pwm_device.value = 0
        set_angle(90)
        sleep(0.5)
        break
    if (current_password == '0000'):
        while True:
            button.when_pressed = button_pressed
            led_G.off()
            for z in range(2):
                led_Y.on()
                sleep(0.3)
                led_Y.off()
                sleep(0.3)
            led_Y.on()
            initiation_password_n = getpass.getpass("Reset your password: ")
            check_password = getpass.getpass("Checking your password: ")
            if (initiation_password_n == '0000'):
                print("Please change the password_ Do not use \"0000\".")
            elif (initiation_password_n == initiation_password):
                print("Please change the password_ Your password was \"%s\"."%initiation_password)
            elif (initiation_password_n == check_password):
                led_Y.off()
                led_G.on()
                print("Successfuly Changed")
                initiation_password = initiation_password_n
                sleep(1)
                led_G.off()
                i = 0
                break
            else:
                led_Y.off()
                led_R.on()
                print("Try again")
                sleep(1)
                led_R.off()
    else: 
        i += 1
        led_G.off()
        led_R.on()
        print("!!!You got %d/3 times wrong!!!" %i)
        sleep(1)
        led_R.off()
        led_G.on()
if (i == 3):
    print("!!!!You cannot come in!!!!")
    led_G.off()
    led_R.on()
    pixels[0] = (255,0,0)
    pixels[1] = (1,0,255)
    pixels[2] = (255,0,0)
    pixels[3] = (1,0,255)
    pixels.show()
    for h in range(len(beep_music)):
        pwm_device.frequency = tones[beep_music[h]]
        pwm_device.value = 0.5 
        sleep(beep_term[h])
        pwm_device.value = 0



#######################################
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
