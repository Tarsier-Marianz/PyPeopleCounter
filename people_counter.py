#-------------------------------------------------------------------------------
# Name:        people_counter.py
# Purpose:
#
# Author:      TARSIER
#
# Created:     18/05/2017
# Copyright:   (c) TARSIER 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import argparse
import datetime
import imutils
import math
import cv2
import numpy as np


def draw_gridlines(img):
    (height, width) = img.shape[:2]
    stepSize = 10;
    for h in range(0,height):
        h =h*20
        cv2.line(img, (0, h), (width, h), (70, 70, 70),1);
        cv2.putText(img,str(h),(0, h), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,255,0), 1)

    for w in range(0,width):
        w =w*20
        cv2.line(img, (w, 0), (w, height), (70, 70, 70),1);
        cv2.putText(img,str(w),(w-20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,255,0), 1)

def draw_gridlinesx(img):
    (height, width) = img.shape[:2]
    stepSize = 10;
    for h in range(0,height):
        h =h*20
        for w in range(0,width):
            w =w*20
            # create horizontal line
            cv2.line(img, (w, h), (width, h), (70, 70, 70),1);
            cv2.putText(img,str(h),(w, h), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,255,0), 1)
            # create vertical line
            cv2.line(img, (w, h), (w, height), (70, 70, 70),1);
            cv2.putText(img,str(w),(w, h), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,255,0), 1)



def testIntersectionIn(frame, x, y):
    res = -450 * x + 400 * y + 157500
    if((res >= -550) and  (res < 550)):
        cv2.putText(frame, str(res),(x, y), cv2.FONT_HERSHEY_SIMPLEX,0.8, (0,255,0), 3)
        print (str(res)+ ' IN')
        return True
    return False



def testIntersectionOut(frame,x, y):
    res = -450 * x + 400 * y + 180000

    if ((res >= -550) and (res <= 550)):
        cv2.putText(frame, str(res),(x, y), cv2.FONT_HERSHEY_SIMPLEX,0.8, (0,255,0), 3)
        print (str(res)+ ' OUT')
        return True

    return False

def main():
    width = 800
    textIn = 0
    textOut = 0

    camera = cv2.VideoCapture("people_counter.mp4")
    #camera = cv2.VideoCapture("people_walk.mp4")
    #camera = cv2.VideoCapture("TownCentreXVID.mp4")

    #camera = cv2.VideoCapture(0)

    firstFrame = None

    # loop over the frames of the video
    while True:
        # grab the current frame and initialize the occupied/unoccupied
        # text
        (grabbed, frame) = camera.read()
        text = "Unoccupied"

        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if not grabbed:
            #print "nothing grabbed"
            break

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=width)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        draw_gridlines(frame)


        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]



        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            area = cv2.contourArea(c)
            #if area < 12000: # for people_counter.mp4
            if area < 2000:
                continue
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv2.drawContours(frame, cnts, -1, (255,0,0),1)
            cv2.putText(frame,str(area),(x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,140,255), 1)

            # for TownCentreXVID.mp4
            #cv2.line(frame, (-350, 0), (width, 350), (250, 0, 1), 2) #blue line
            #cv2.line(frame, (-450, 0), (width, 400), (0, 0, 255), 2)#red line

            # for people_counter.mp4
            cv2.line(frame, (width / 2, 0), (width, 450), (250, 0, 1), 2) #blue line
            cv2.line(frame, (width / 2 - 50, 0), (width - 50, 450), (0, 0, 255), 2)#red line

            # for people_walk.mp4
            #cv2.line(frame, (width -100, 0), (5, width-10 ), (250, 0, 1), 2) #blue line
            #cv2.line(frame, (width - 200, 0), (5, width-80), (0, 0, 255), 2)#red line



            rectagleCenterPont = ((x + x + w) /2, (y + y + h) /2)
            cv2.circle(frame, rectagleCenterPont, 1, (0, 0, 255), 5)
            cv2.putText(frame,str(rectagleCenterPont),rectagleCenterPont, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,140,255), 1)

            if(testIntersectionIn(frame,(x + x + w) / 2, (y + y + h) / 2)):
                textIn += 1
                cv2.putText(frame,'IN',rectagleCenterPont, cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 3)

            if(testIntersectionOut(frame,(x + x + w) / 2, (y + y + h) / 2)):
                textOut += 1
                cv2.putText(frame,'OUT',rectagleCenterPont, cv2.FONT_HERSHEY_SIMPLEX,2, (0,255,0), 3)

            # draw the text and timestamp on the frame

            # show the frame and record if the user presses a key
            # cv2.imshow("Thresh", thresh)
            # cv2.imshow("Frame Delta", frameDelta)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.putText(frame, "In: {}".format(str(textIn)), (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, "Out: {}".format(str(textOut)), (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        cv2.imshow("Security Feed", frame)


    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()




