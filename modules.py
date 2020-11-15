'''
The following file contains code for
the compnents: motor, camera, servo, ultrasonic sensor

'''
class motor():
    def __init__(self, pin1, pin2, pin3, GPIO):
        #for motor(in_1, in_2) (1,1) = stop
        # (1,0) = backwards (0,1) = forwards
        self.in_1 = pin1
        self.in_2 = pin2 #pin1 and pin2 are used for direction control of motor
        self.GPIO = GPIO #library for rpi pin initialization
        self.pwm_pin = pin3 #pin for the pulse width modulations 
        
        self.dir = 0 #dirction of the motor
        
        GPIO.setup(self.in_1, GPIO.OUT)
        GPIO.setup(self.in_2, GPIO.OUT)
        GPIO.setup(self.pwm_pin, GPIO.OUT) #set up pins for output
        self.pmw = GPIO.PWM(self.pwm_pin, 1000) #set up pwm pin
     
        GPIO.output(self.in_1, GPIO.HIGH) #initial state is stoped
        GPIO.output(self.in_2, GPIO.HIGH)
        self.pmw.start(12.5)  #THIS IS USED TO CONTORL SPEED! higher value = faster
        
    #direction functions    
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
    def cleanup(self):
        self.pmw.stop()
        
#code for ultrasonic sensor
class sensor():
    def __init__(self, pin1, pin2, GPIO):
        #pin initialization and set up
        self.trig = pin1
        self.echo = pin2
        self.GPIO = GPIO
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        
        #function for determining distance
    def get_dist(self, time):
        #pulse trigger
        self.GPIO.output(self.trig, self.GPIO.HIGH) 
        time.sleep(.00001)
        self.GPIO.output(self.trig, self.GPIO.LOW)
        
        pulse_end = 0
        pusle_start = 0 #variables to store start and stop time
        
        while self.GPIO.input(self.echo) == 0: #wait for input pin to turn on
            pulse_start = time.time()
        while self.GPIO.input(self.echo) == 1: #wait for return signal
            pulse_end = time.time()

        return round((pulse_end - pulse_start) * 17150, 2) #calculate distance

#code for servo
#servo changes angle based on duty cycle 
class servo():
    def __init__(self, pin, GPIO):
        #initialize pins
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
        
    #turns to an angle between 0 and 180
    def turn_angle(self,angle):
        if(angle < 0):
            angle = 0
        elif(angle > 180):
            angle = 180
        fraction = angle/180.0
        self.pmw.ChangeDutyCycle(12.5*fraction)
    def cleanup(self):
        self.pmw.stop()
   
#class for camera
class camera():
    def __init__(self, cv2):
        #initialize variables
        self.cv2 = cv2
        self.cap = self.cv2.VideoCapture(0)
        ret, self.frame = self.cap.read()
        self.gray_frame = self.cv2.cvtColor(self.frame, self.cv2.COLOR_BGR2GRAY)
    
    def get_image(self):
        ret, self.frame = self.cap.read()
        return self.frame
    
    def get_gray(self):
        ret, self.frame = self.cap.read()
        self.gray_frame = self.cv2.cvtColor(self.frame, self.cv2.COLOR_BGR2GRAY)
        return self.gray_frame
    def cleanup(self):
        self.cap.release()
