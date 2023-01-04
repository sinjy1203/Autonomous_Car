import cv2
import numpy as np
from pathlib import Path

drawing_fname = Path('./data/drawing_chess/draw_undistortion.jpg')
raw_fname = Path("./data/undistortion_chess/undistortion_img.jpg")


def mouse_event(event, x, y, flags, param):
    global pos, cnt
    if event == cv2.EVENT_FLAG_LBUTTON and cnt == 0:
        pos = (x, y)
        cnt += 1

    if event == cv2.EVENT_FLAG_LBUTTON and cnt == 1:
        param = cv2.line(param, pos, (x, y), (0, 0, 255), 1)
        cv2.imshow("draw", param)
        cv2.imwrite(str(drawing_fname), param)


pos = (0, 0)
cnt = 0
src = cv2.imread(str(raw_fname))
cv2.imshow("draw", src)
cv2.setMouseCallback("draw", mouse_event, src)
cv2.waitKey()