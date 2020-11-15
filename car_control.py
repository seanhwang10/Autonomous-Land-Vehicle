'''
THINGS THAT NEED TO BE EVALUTED/PROGRAMMED:
1. Necesary speed of the motor to make the car move at a crusing speed
2. Integrate all components to work together
    i.e
    a. wheels and ultrasonic sensor servo move in unison based on
       angle (given by image processing code)
    b. ulstrasonic sensor stops motor when detects object
3. Find a way to gracefully exit the program at end of execution, so
clean up functions are always able to run before program terminates
4. How to run this executable (once complete) as defualt program so that
it automatically runs when rpi is powered.
'''

print("running set up")
#import necesary files
import modules
import cv2
import RPi.GPIO as GPIO
import time

#the following section creates objects of the various
#components with specefic pin assignments
cam = modules.camera(cv2)
sonar_servo = modules.servo(18, GPIO)
steering = modules.servo(17, GPIO)
ultra_servo = modules.servo(7, GPIO)
sonar = modules.sensor(14,15,GPIO)
motor = modules.motor(2,3,4, GPIO)
print("set up copmlete")

#dummy function to represent a function that can calculate
#the trajectory for the line to be followed
def get_dir():
    return 90
    
#function that checks if an obstacle is in the path of the sensor
def check_obstacle():
    '''Possible Change
        Change evalution of obstacle from calculating average read
        distance to counting number of read values in range
    '''
    total = 0 #variable to total all distances
    for i in range(0,5): #preform 5 iterations summing distance values
        total = total + sonar.get_dist(time)
    print(total/5) #print averaged distance
    if(total/5 < 10): #if the average is below 10 cm returns false b/c obstacle
        return 0
    else:
        return 1 
    
motor_state = 1 #contorl direction of car
dirc = get_dir()

#following is code to test various functions 
for i in range(1,300): 
    if(motor_state == 1):
        motor.forward()
    elif(motor_state == -1):
        motor.backwards()
    else:
        motor.stop()
    
    steering.turn_angle(dirc) #turns front wheels
    
    ultra_servo.turn_angle(dirc) #turns servo for ultrasonic sensor
    
    motor_state = check_obstacle() #checks for obstacle
    
    

 
#clean up for exit
cam.cleanup()
GPIO.cleanup()                                       
sonar_servo.cleanup()
motor.cleanup()

'''
#Demmo of evrything working
sonar_servo.turn_left()
time.sleep(1)
sonar_servo.turn_right()
time.sleep(1)

steering.turn_left()
time.sleep(1)
steering.turn_right()
time.sleep(1)

time.sleep(1)
motor.forward()
time.sleep(1)
motor.stop()

time.sleep(1)
motor.backwards()
time.sleep(1)
motor.stop()

while(True):
    cv2.imshow("wind",cam.get_gray())
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
for i in range(0,5):
    cv2.waitKey(1)
'''




