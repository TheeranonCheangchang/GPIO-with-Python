import RPi.GPIO as GPIO
import time

# กำหนดพินที่เชื่อมต่อกับ RGB LED
RED_PIN = 11
GREEN_PIN = 10
BLUE_PIN = 8

# กำหนดพินที่เชื่อมต่อกับปุ่มสวิตช์
SWITCH_PIN = 15

# ตั้งค่า GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # ใช้ pull-up resistor

# สร้าง PWM อินสแตนซ์
pwm_red = GPIO.PWM(RED_PIN, 1000)  # ความถี่ 1000Hz
pwm_green = GPIO.PWM(GREEN_PIN, 1000)
pwm_blue = GPIO.PWM(BLUE_PIN, 1000)

# เริ่มการทำงานของ PWM
pwm_red.start(0)
pwm_green.start(0)
pwm_blue.start(0)

# ตัวแปรเพื่อเก็บสถานะสี
current_color = 0

try:
    while True:
        if GPIO.input(SWITCH_PIN) == GPIO.LOW:  # ตรวจสอบการกดปุ่ม
            # เปลี่ยนสีตาม current_color
            if current_color == 0:
                for i in range(0, 101, 5):  # 0% ถึง 100% ความสว่าง
                    pwm_red.ChangeDutyCycle(100 - i)
                    pwm_green.ChangeDutyCycle(i)
                    pwm_blue.ChangeDutyCycle(0)
                    time.sleep(0.05)
                current_color = 1
            elif current_color == 1:
                for i in range(0, 101, 5):
                    pwm_red.ChangeDutyCycle(0)
                    pwm_green.ChangeDutyCycle(100 - i)
                    pwm_blue.ChangeDutyCycle(i)
                    time.sleep(0.05)
                current_color = 2
            elif current_color == 2:
                for i in range(0, 101, 5):
                    pwm_red.ChangeDutyCycle(i)
                    pwm_green.ChangeDutyCycle(0)
                    pwm_blue.ChangeDutyCycle(100 - i)
                    time.sleep(0.05)
                current_color = 0
            # รอจนกว่าปุ่มจะถูกปล่อย
            while GPIO.input(SWITCH_PIN) == GPIO.LOW:
                time.sleep(0.1)
        else:
            # ทำให้ RGB LED มีสีคงที่เมื่อปุ่มไม่ถูกกด
            pwm_red.ChangeDutyCycle(0)
            pwm_green.ChangeDutyCycle(0)
            pwm_blue.ChangeDutyCycle(0)
            time.sleep(0.1)

except KeyboardInterrupt:
    pass
finally:
    # ปิดการทำงานของ PWM และทำความสะอาด GPIO
    pwm_red.stop()
    pwm_green.stop()
    pwm_blue.stop()
    GPIO.cleanup()
    print("\nBye")
