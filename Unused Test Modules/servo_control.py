class servo():
    def __init__(self, pin, GPIO):
        #initialize pin number
        self.pin = pin
        self.GPIO = GPIO
        
        #create pmw pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pmw = GPIO.PWM(self.pin, 50)
        self.pmw.start(7.5)
    def turn_left(self):
        self.pmw.ChangeDutyCycle(12.5);
    
    def turn_right(self):
        self.pmw.ChangeDutyCycle(2.5);
    
    def turn_straight(self):
        self.pmw.ChangeDutyCycle(7.5);
        
    def turn_angle(self,angle):
        if(angle < 0):
            angle = 0
        elif(angle > 180):
            angle = 180
        fraction = angle/180.0
        self.pmw.ChangeDutyCycle(12.5*fraction)
        
def main():
    import RPi.GPIO as GPIO
    import time
    GPIO.setmode(GPIO.BCM)
    serv = servo(18, GPIO)
    try:
        while True:
            serv.turn_right()
            time.sleep(10)
            serv.turn_left() 
            time.sleep(10)
    except KeyboardInterrupt:
        serv.pmw.stop()
        GPIO.cleanup()
main()
    
    
