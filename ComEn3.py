import RPi.GPIO as GPIO
import time 

LED = 18
SW = 22
count = 0
toggle = True
GPIO.setmode(GPIO.BCM)
GPIO.setup(SW, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(LED, GPIO.OUT)
try:
    while True :
        if GPIO.wait_for_edge(SW, GPIO.FALLING):
            toggle = not(toggle)
            count = count + 1
            GPIO.output(LED, toggle)
            time.sleep(1)
            print(f"Button pressed {count}")
except KeyboardInterrupt:
    GPIO.cleanup()
print("\nBye")
        
    

