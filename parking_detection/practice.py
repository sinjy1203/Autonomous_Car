##
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt

path = "C:/Users/sinjy/PycharmProjects/GIGACHA/parking_detection/video_data/output302.avi"
cap = cv2.VideoCapture(path)

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        cv2.imshow('frame', frame)
    if cv2.waitKey(0) & 0xFF == ord('c'):
        cv2.imwrite('C:/Users/sinjy/PycharmProjects/GIGACHA/parking_detection/data/corner2.png', frame)
        break

cap.release()
cv2.destroyAllWindows()


##

