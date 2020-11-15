class motor():
    def __init__(self, pin1, pin2, pin3, GPIO):
        #for motor(in_1, in_2) (1,1) = stop
        # (1,0) = backwards (0,1) = forwards
        self.in_1 = pin1
        self.in_2 = pin2
        self.GPIO = GPIO
        self.pwm_pin = pin3
        
        self.dir = 0 
        
        GPIO.setup(self.in_1, GPIO.OUT)
        GPIO.setup(self.in_2, GPIO.OUT)
        GPIO.setup(self.pwm_pin, GPIO.OUT)
        self.pmw = GPIO.PWM(self.pwm_pin, 70)
     
        GPIO.output(self.in_1, GPIO.HIGH)
        GPIO.output(self.in_2, GPIO.HIGH)
        self.pmw.start(12.5)  
        
    def forward(self):
        self.GPIO.output(self.in_1, self.GPIO.LOW)
        self.GPIO.output(self.in_2, self.GPIO.HIGH)
        self.dir = 1
    def backwards(self):
        self.GPIO.output(self.in_1, self.GPIO.HIGH)
        self.GPIO.output(self.in_2, self.GPIO.LOW)
        self.dir = -1
    def stop(self):
        self.GPIO.output(self.in_1, self.GPIO.HIGH)
        self.GPIO.output(self.in_2, self.GPIO.HIGH)
        self.dir = 0
        
def main():
    import RPi.GPIO as GPIO 
    import time
    GPIO.setmode(GPIO.BCM)
    mot = motor(14,15,18, GPIO)
    try:
        while True:
            mot.forward()
            time.sleep(2) 
            mot.stop()
            time.sleep(2)
            mot.backwards() 
            time.sleep(2) 
    except KeyboardInterrupt:
        GPIO.cleanup()   
main()
