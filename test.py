import numpy as np
import cv2
from skimage import measure

def nothing(x):
    pass

def edit_exposure(pos):
    global cap
    cap.set(cv2.CAP_PROP_EXPOSURE, pos)  # default: 15
    print("exposure: {}".format(cap.get(cv2.CAP_PROP_EXPOSURE)))

cap = cv2.VideoCapture(1)
cv2.namedWindow('ord')
# cv2.createTrackbar("auto_exposure", "ord", 0, 100, lambda x : x)
cv2.createTrackbar("exposure", "ord", 0, 100, edit_exposure)
# cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3) # 1, # default: 21
# cap.set(cv2.CAP_PROP_EXPOSURE, 15) # default: 15

ret, img = cap.read()

while True:
    # auto_exposure = cv2.getTrackbarPos("auto_exposure", "ord")
    # exposure = cv2.getTrackbarPos("exposure", "ord")
    # print(exposure)
    # cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, auto_exposure) # 1, # default: 21
    # cap.set(cv2.CAP_PROP_EXPOSURE, exposure) # default: 15
    # auto_exposure_get = cap.get(cv2.CAP_PROP_AUTO_EXPOSURE)
    # exposure_get = cap.get(cv2.CAP_PROP_EXPOSURE)
    # print("exposure: {}".format(exposure_get))
    ret, img = cap.read()
    cv2.imshow('ord', img)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()