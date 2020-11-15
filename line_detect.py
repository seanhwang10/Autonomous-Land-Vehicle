import cv2
import numpy as np
import time
'''
Overall strategy for building trajectory:
1. analyze the image looking for first instance of correctly colored
    pixel and stores col location in array
2. averages col location for top half and bottom half of array
3. uses averages as points to create a line

KNOWN ISSUES:
1. If a color pixel is not in a row i.e. line only present in half the photo
the average values are thwon off.
2. Glare from lights changes the color of the image line causing for
bad data

TO fix: Find a way to only include "good" data points in average
calculations
ONCE FIEXED: a trajectory for the cart to follow can be calculated

SUGGESTIONS: change array to be a list to implement a stack, push on stack
good data points and pop from stack for calculating average points
'''

cap = cv2.VideoCapture(0) #starts feed of camera
#important code will error out if no camera is connected to rpi

cap.set(3, 200) #initialize values for camera

while(True):
    ret, img = cap.read() #get image frame from camera
    
    points = [0 for row in range(img.shape[0]/2)]
    #initialize array of zeros with size of half the hieght of image
    
    count = 0 #count number of points that match color of line in a row
    
    
    for i in range(0,img.shape[0],2): #itterate through every other row of pixels
        for j in range(0,img.shape[1],2): #itterate thourhg every other column in row
            if(abs(img[i][j][0] - 175)< 30 and abs(img[i][j][1] - 100)< 30 and abs(img[i][j][2] - 100)< 30):
                #^compares pixel values to see if it is close to line color
                
                img[i][j] = [0,0,0] #colors pixel black for visual purposes
                points[i/2] = j  #stores col number
                count = count + 1 #adds one to count
                break #stops itteration of that row
            
    #color of current line (175, 100, 100)
    
    #calculating average values
    top_avg = 0; #average column value for top half of line
    bot_avg = 0; #average column value for bottom half of line
    for i in range(0,img.shape[0]/4): #itterate through list of stored col
        top_avg = top_avg + points[i] #sum all values in first half of points
        bot_avg = bot_avg + points[i+img.shape[0]/4] #sum of all values of second half of poitns
    top_avg  = top_avg / (img.shape[0]/4) #average top values
    bot_avg = bot_avg / (img.shape[0]/4) #average bottom values 
    cv2.line(img,(top_avg,img.shape[0]/6),(bot_avg,5*img.shape[0]/6),(0,0,255),5)
    #^draws line on image
    cv2.imshow('frame',img) #displays image
    
    if cv2.waitKey(1) & 0xFF == ord('q'): #if q on keyboard is pressed stop execution
        break
cv2.destroyAllWindows() #closes opened window