import RPi.GPIO as GPIO
import time 

pmwPin = 18
speed = 50
GPIO.setmode(GPIO.BCM)

GPIO.setup(pmwPin, GPIO.OUT)
pmw = GPIO.PWM(pmwPin, speed)
pmw.start(7.5)

try:
    while True:
        pmw.ChangeDutyCycle(7.5)
        time.sleep(5)
        pmw.ChangeDutyCycle(2.5)
        time.sleep(5)
        #pmw.ChangeDutyCycle(12.5)
        time.sleep(5)  
except KeyboardInterrupt:
    pmw.stop()
    GPIO.cleanup()
