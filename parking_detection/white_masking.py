import cv2
import numpy as np
import matplotlib.pyplot as plt

frame = cv2.imread("./data/cross0.png")
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# define range of blue color in HSV
sensitivity = 40
lower_white = np.array([0,0,255-sensitivity])
upper_white = np.array([255,sensitivity,255])

#How to define this range for white color


# Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv, lower_white, upper_white)
# Bitwise-AND mask and original image
res = cv2.bitwise_and(frame,frame, mask= mask)

cv2.imshow('frame',frame)
cv2.imshow('mask',mask)
cv2.imshow('res',res)
cv2.waitKey(0)