# coding=utf-8
import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
#a classi created that does simple stuff like creating the track bars.
#or creating the mask
from opencvBasic import opencvBasic
import math


#finds the distence between 2 points
def distence(x1,x2):
    return math.fabs(x1-x2)


def sort_contours(cnts, method="left-to-right"):
    # initialize the reverse flag and sort index
    reverse = False
    i = 0

    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True

    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1

    # construct the list of bounding boxes and sort them from top to
    # bottom
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),key=lambda b: b[1][i], reverse=reverse))
    # return the list of sorted contours and bounding boxes
    return cnts

#finds the bigger distence between points 0 and 1 in 2 rects
#and with that infomation returns 0 or 1
def findSmallest(midFrame,midx):
    smallest = 1000
    i = 0
    temp = 0
    for x in midx:
        dis = math.fabs(x - midFrame)
        if dis < smallest:
            smallest = dis
            midX = x
            temp = i
        i +=1
    return midX, temp
#returns starting point but better
def getStartingPoint2(cnts):
    i = 0
    #gets the delta X and Y and finds the slope
    [dx, dy] = cv2.fitLine(filterCnts[i], cv2.DIST_L2, 0, 0.01, 0.01)[:2]
    m = dy / dx
    #the y axis is inverted so the slope is also inverted
    if m < 0:
        i =1
    return i
#returns starting point but worse
#dont use this function
def getStartingPoint1(cnts):
    dis = []
    j = 0
    if len(cnts) > 2:
        for i in range(2):
            rect = cv2.minAreaRect(cnts[i])
            points = cv2.boxPoints(rect)
            points = np.int0(points)
            dis.append(distence(points[0],points[1]))
        if dis[0] < dis[1]:
            j = 1
    return j


winName = "sliders"
#creates a list of the img names from
#the #"v" folder
path = "v/"
images = [f for f in listdir(path) if isfile(join(path, f))]

#creates the class obj
t = opencvBasic(winName)
debug = True
# cap = cv2.VideoCapture('http://root:root@10.45.86.12/mjpg/video.mjpg')
# cap = cv2.VideoCapture(0)

#creates the sliders
sliders = t.createTrackBars(winName)
#the img counter
#the number of file in the v folder
imgC = 0
half_fov = 27.7665349671
tan = math.tan(math.radians(half_fov))
while (imgC <len(images)):
    # _ ,frame = cap.read()
    # מובן מעליו
    frame = cv2.imread("v/"+images[imgC])
    f_height , f_width , _ = frame.shape

    # upper = t.Upper(winName)
    # lower = t.Lower(winName)
    upper = np.array([218,255,111])
    lower = np.array([51,126,0])
    midFrame = f_width/2
    mask = cv2.inRange(frame,lower,upper)
    bitImg = cv2.bitwise_and(frame,frame,mask = mask )
    contours,_ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    filterCnts = []
    #filter the contuores
    for cnt in contours:
        S = cv2.contourArea(cnt)
        if S > 100:
            filterCnts.append(cnt)
    #if the number of filter contours makes sense
    if len(filterCnts) > 1 and len(filterCnts) < 25:
        #filter the contours from right to left
        filterCnts = sort_contours(filterCnts, method="right-to-left")
        #get the while loop's starting point based on the
        #first contoure oriantion
        i = getStartingPoint2(filterCnts)
        cX = [0,0]
        #a list of all the mid x values from the pic
        midx = []
        dis = []
        #finds the mid points. and add them to a list
        while i < len(filterCnts)-1:
            rect = cv2.minAreaRect(filterCnts[i])
            points = cv2.boxPoints(rect)
            points = np.int0(points)
            x1 = points[1][0]
            rect = cv2.minAreaRect(filterCnts[i+1])
            points = cv2.boxPoints(rect)
            points = np.int0(points)
            x2 = points[3][0]
            midx.append((x1+x2)/2)
            dis.append(distence(x1,x2))
            if debug:
                cv2.line(bitImg,(int((x1+x2)/2),0),(int((x1+x2)/2),1000),(0,0,255),2)
            i += 2
        #finds the mid x with the clousest distence
        midxAvg,i = findSmallest(midFrame,midx)
        tan_angle = ((midxAvg - midFrame) * tan) / (midFrame)  # tangens of angle alfa
        Rangle = math.degrees(math.atan(tan_angle))  # tangens of angle alfa
        angle = math.degrees(Rangle)
        print angle
        dis = dis[i]
        d = (20*f_width)/(2*dis*tan_angle)
        print d
        # print angle
    k = cv2.waitKey(1)
    if debug:
        cv2.line(bitImg,(int(midFrame),0),(int(midFrame),1000),(255,0,0))
        cv2.imshow(winName,sliders)
        cv2.imshow("bitImg",bitImg)
        cv2.imshow("mask",mask)
        if imgC < 0 or imgC >= len(images)-1:
            imgC = 0
        if k == 87 or k == 119:
            imgC += 1
        if k == 83 or k== 115:
            imgC -= 1
        if k == 27:
            break
cv2.destroyAllWindows()
