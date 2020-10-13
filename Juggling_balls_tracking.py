# Code from PyImageSearch 'Ball Tracking with OpenCV'
### https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/ ###

from imutils.video import VideoStream
from collections import deque
import numpy as np
import argparse
import imutils
import time
import cv2


# construct the argument parser and parse the arguments:
ap = argparse.ArgumentParser()
ap.add_argument('-v', '--video', required=False, help='path to the input video file')
ap.add_argument('-b', '--buffer', required=True, type=int, default=32, help='buffer or length of the tail')
ap.add_argument('-m', '--mask', required=True, type=int, default=True, help='True for visualize mask, False for dont visualize')
args = vars(ap.parse_args())

# define color boundaries conditions in a HSV format,
# (defined values for green color)
# green:  (29, 86, 6)  (64, 255, 255)
lowerColor = (65, 86, 6)
upperColor = (85, 255, 255)

# initialize position vector
pts = deque(maxlen=args['buffer'])

# check if users chose video file or videostream
if not args.get('video', False):
    vs = VideoStream(src=0).start()
else:
    vs = cv2.VideoCapture(args['video'])

# time for warming up the camera or video
time.sleep(2.0)
# just a secondary variable
balls_before=0

# loop for each video frame 
while True:

    # read the frame
    frame = vs.read()

    # if user chose existed video
    if args.get('video', False):
        frame = frame[1]

    # in case it was a video, check if we have reached the end of that
    if frame is None:
        break
    
    # resize frame, blur it and convert it to the HSV format
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, ksize=(11,11), sigmaX=0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # create the mask using inRange method. Every pixel inside of both boundaries will be 1. In other case will be 0.
    mask = cv2.inRange(hsv, lowerb=lowerColor, upperb=upperColor)
    mask = cv2.erode(mask, kernel=None, iterations=5)
    mask = cv2.dilate(mask, kernel=None, iterations=5)

    # show the mask depending on preference user's
    if args['mask'] == 1:
        cv2.imshow('mask', mask)

    # now that we have the mask, we need to find every contours of the mask.
    # In that case, we only want contours with a 'relative big size'
    all_cnts = cv2.findContours(mask, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    all_cnts = imutils.grab_contours(all_cnts)
    
    #if there are contours
    if len(all_cnts) > 0:

        cnts = []
        # we only want the largest contours
        for cnt in all_cnts:
            ((x,y), radius) = cv2.minEnclosingCircle(cnt)
            
            # we grab the real contours
            if radius > 5:
                cnts.append(cnt)


        # number of diferent balls/contours
        balls = len(cnts)

        # we clean the points vector if a ball go in/out of the frame
        if balls_before != balls:
            pts.clear()
            while len(pts) < balls:
                pts.append(deque(maxlen=args['buffer']))

        
        for ball, cnt in enumerate(cnts): 
            try:
                # calculate the center = (x,y) and radius of the contour
                ((x,y), radius) = cv2.minEnclosingCircle(cnt)

                # calculate the distance from (x,y) to each ball
                # we chose the nearest ball to (x,y) point
                distance = []
                for index in range(0, balls):
                    distance.append((x - pts[index][0][0])**2 + (y - pts[index][0][1])**2)
                if min(distance) < 4*radius*radius:
                    thatball = distance.index(min(distance))

                # add new point to the correct ball
                pts[thatball].appendleft((int(x), int(y)))

                # draw contour
                cv2.circle(frame, center=(int(x),int(y)), radius=int(radius), color=(0,255,255), thickness=2)
                # draw center
                cv2.circle(frame, center=(int(x),int(y)), radius=5, color=(0,0,255), thickness=-1)
                # specify the ball number
                cv2.putText(frame, str(thatball+1), org=(int(x-10),int(y-15)), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255,0,0), thickness=2)
            
                # draw tails of balls
                cv2.putText(frame, text='Balls:'+ str(balls), org=(15,28), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255,0,0), thickness=2)
                for i in range(1, len(pts[thatball])):
                    if pts[thatball][i] is None or pts[thatball][i-1] is None:
                        continue
                    thickness = int(np.sqrt(args['buffer']/float(i+1))*2.5)
                    cv2.line(frame, pt1=pts[thatball][i-1], pt2=pts[thatball][i], color=(0,0,255), thickness=thickness)
                    
            # only for first iteration
            # because during first iteration we haven't points to calculate distances
            except:
                pts[ball].appendleft((int(x), int(y)))

        # update number of balls
        balls_before = balls

    # show the frame with identified balls and paths
    cv2.imshow('frame', frame)
    
    # key to stop the program
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# a bit of cleaning :)
if not args.get('video', False):
    vs.stop()
else:
    vs.release()

cv2.destroyAllWindows()