import cv2
import numpy as np
class opencvBasic:
    def __init__(self,winName):
        self.minh = cv2.getTrackbarPos("h min", winName)
        self.mins = cv2.getTrackbarPos("s min", winName)
        self.minv = cv2.getTrackbarPos("v min", winName)

        self.maxh = cv2.getTrackbarPos("H max", winName)
        self.maxs = cv2.getTrackbarPos("S max", winName)
        self.maxv = cv2.getTrackbarPos("V max", winName)
    def nothing(self,x):
        pass

    def Lower(self,winName):
        lower = np.array(
            [cv2.getTrackbarPos("h min", winName),
             cv2.getTrackbarPos("s min", winName),
             cv2.getTrackbarPos("v min", winName)])
        return lower

    def Upper(self,winName):
        Upper = np.array(
            [cv2.getTrackbarPos("H max", winName),
             cv2.getTrackbarPos("S max", winName),
             cv2.getTrackbarPos("V max", winName)])
        return Upper

    def createTrackBars(self,winName):

        # Create a black image, a window
        img = np.zeros((1 , 400, 3), np.uint8)
        cv2.namedWindow(winName)

        # create trackbars for color change
        cv2.createTrackbar('h min', winName, 0, 255, self.nothing)
        cv2.createTrackbar('s min', winName, 0, 255, self.nothing)
        cv2.createTrackbar('v min', winName, 0, 255, self.nothing)
        cv2.createTrackbar('H max', winName, 0, 255, self.nothing)
        cv2.createTrackbar('S max', winName, 0, 255, self.nothing)
        cv2.createTrackbar('V max', winName, 0, 255, self.nothing)
        return img

    def endOfCode(self):
        print("["+ str(self.minh) + ","+ str(self.mins) + ","+ str(self.minv)+"]")
        print("[" + str(self.maxh) + "," + str(self.maxs) + "," + str(self.maxv) + "]")

    def createMask(self,Img,slidersWinName):
        hsvImg = cv2.cvtColor(Img, cv2.COLOR_BGR2HSV_FULL)
        mask = cv2.inRange(hsvImg, self.Lower(slidersWinName), self.Upper(slidersWinName))
        final = cv2.bitwise_and(Img,Img, mask=mask)
        return final
    def returnMask(self,Img,slidersWinName):
        hsvImg = cv2.cvtColor(Img, cv2.COLOR_BGR2HSV_FULL)
        mask = cv2.inRange(hsvImg, self.Lower(slidersWinName), self.Upper(slidersWinName))
        return mask
    def GetLowerAndUpper(self):
        return self.Lower()