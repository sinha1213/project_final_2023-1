import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
servo_pin = 18
button_pin = 24  # 예시로 버튼 핀 번호 설정 (실제 사용하는 핀 번호로 변경해야 함)

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # 버튼이 풀다운 저항으로 연결된 경우

# PWM 객체 생성
pwm = GPIO.PWM(servo_pin, 50)  # 주파수 50Hz로 설정

# PWM 시작
pwm.start(0)

def set_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

try:
    while True:
        if GPIO.input(button_pin) == GPIO.HIGH:
            # 버튼이 눌렸을 때
            set_angle(90)  # 예시로 90도로 설정
            time.sleep(0.5)  # 버튼 리바운스 방지를 위한 잠시의 대기
            while GPIO.input(button_pin) == GPIO.HIGH:
                time.sleep(0.1)  # 버튼이 떨어질 때까지 대기
            set_angle(0)  # 버튼이 떨어지면 초기 위치로 돌아감

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
