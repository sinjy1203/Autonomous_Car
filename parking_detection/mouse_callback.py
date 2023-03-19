import cv2
import numpy as np


def mouse_event(event, x, y, flags, param):
    global radius

    if event == cv2.EVENT_FLAG_LBUTTON:
        print(x, y)

src = cv2.imread("./data/cross15.png")

cv2.imshow("draw", src)
cv2.setMouseCallback("draw", mouse_event, src)
cv2.waitKey()