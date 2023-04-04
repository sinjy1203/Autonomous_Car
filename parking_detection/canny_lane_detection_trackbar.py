import cv2
import numpy as np
import matplotlib.pyplot as plt

def callback(x):
    print(x)

def lane_detection(img, l, u, threshold, minLineLength, maxLineGap):
    zeros = np.zeros_like(img)
    img = cv2.medianBlur(img, ksize=13)
    edges = cv2.Canny(img, l, u)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=threshold, minLineLength=minLineLength, maxLineGap=maxLineGap)
    print(len(lines))
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(zeros, (x1, y1), (x2, y2), (255, 255, 255), 2)
    return zeros


img = cv2.imread("C:/Users/sinjy/PycharmProjects/GIGACHA/parking_detection/data/parking_line.png") #read image as grayscale
img = cv2.resize(img, (720, 480))
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
result = lane_detection(img, 85, 255, 10, 20, 2)

cv2.namedWindow('image') # make a window with name 'image'
cv2.createTrackbar('L', 'image', 0, 255, callback) #lower threshold trackbar for window 'image
cv2.createTrackbar('U', 'image', 0, 255, callback) #upper threshold trackbar for window 'image
cv2.createTrackbar('threshold', 'image', 0, 100, callback)
cv2.createTrackbar('minLineLength', 'image', 0, 100, callback)
cv2.createTrackbar('maxLineGap', 'image', 0, 100, callback)


while(1):
    numpy_horizontal_concat = np.concatenate((img, result), axis=1) # to display image side by side
    cv2.imshow('image', numpy_horizontal_concat)
    k = cv2.waitKey(1) & 0xFF
    if k == 27: #escape key
        break
    l = cv2.getTrackbarPos('L', 'image')
    u = cv2.getTrackbarPos('U', 'image')
    threshold = cv2.getTrackbarPos('threshold', 'image')
    minLineLength = cv2.getTrackbarPos('minLineLength', 'image')
    maxLineGap = cv2.getTrackbarPos('maxLineGap', 'image')

    result = lane_detection(img, l, u, threshold, minLineLength, maxLineGap)

cv2.destroyAllWindows()