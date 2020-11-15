class sensor():
    def __init__(self, pin1, pin2, GPIO):
        self.trig = pin1
        self.echo = pin2
        self.GPIO = GPIO
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
    def get_dist(self, time):
        self.GPIO.output(self.trig, self.GPIO.HIGH)
        time.sleep(.00001)
        self.GPIO.output(self.trig, self.GPIO.LOW)
        while self.GPIO.input(self.echo) == 0:
            pulse_start = time.time()
        while self.GPIO.input(self.echo) == 1:
            pulse_end = time.time()
        return round((pulse_end - pulse_start) * 17150, 2)
    
def main():
    import RPi.GPIO as GPIO 
    import time
    GPIO.setmode(GPIO.BCM)
    ultra = sensor(15,18, GPIO)
    try:
        while True:
            print(ultra.get_dist(time))
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()  
main()  
