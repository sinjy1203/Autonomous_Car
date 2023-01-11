# from __future__ import (
#     division, absolute_import, print_function, unicode_literals)

import cv2 as cv
import numpy as np


def white_balance(img):
    result = cv.cvtColor(img, cv.COLOR_BGR2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])
    result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result = cv.cvtColor(result, cv.COLOR_LAB2BGR)
    return result

# W, H = 1900, 1090
cap = cv.VideoCapture(0)
# cap.set(cv.CAP_PROP_FRAME_WIDTH, W)
# cap.set(cv.CAP_PROP_FRAME_HEIGHT, H)

while True:
    ret, img = cap.read()
    final = np.hstack((img, white_balance(img)))
    # final = white_balance(img)
    print(final.shape)
    cv.imshow('AWB', final)
    if cv.waitKey(20) & 0xFF == ord('q'):
        break

# cap.release()
cv.destroyAllWindows()