import cv2
import sys
from pathlib import Path
import time
import numpy as np
from undistort import UnDistort


data_dir = Path('img_data')
if not data_dir.exists():
    data_dir.mkdir()
param_dir = Path('camera_param')


# Load Web Camera
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)


# cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3) # auto mode
# cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1) # manual mode
cap.set(cv2.CAP_PROP_EXPOSURE, -3) # -1 to -13
if not (cap.isOpened()):
    print("File isn't opend!!")

w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # width
h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # height

# Load frame and Save it
while (True):  # Check Video is Available
    ret, frame = cap.read()  # read by frame (ret=TRUE/FALSE)s
    if ret:
        cv2.imshow('img', frame)
        if cv2.waitKey(1) == ord('c'):
            img = cv2.imwrite(str(data_dir / 'square.png'), frame)
            print('save square.png')
            break

        if cv2.waitKey(1) == ord('q'):  # wait 10ms until user input 'esc'
            break
    else:
        print("ret is false")
        break

cap.release()  # release memory
cv2.destroyAllWindows()  # destroy All Window


# mouse callback to get pixel
img_square = cv2.imread(str(data_dir / 'square.png'))

# undistort
mtx, dist = np.load(str(param_dir / 'mtx.npy')), np.load(str(param_dir / 'dist.npy'))
img_square_u = UnDistort(img_square, mtx, dist, img_square.shape[:2][::-1])
cv2.imwrite(str(data_dir / 'square_u.png'), img_square_u)
# exit()
points_2D = []

def mouse_event(event, x, y, flags, param):
    global points_2D

    if event == cv2.EVENT_FLAG_LBUTTON:
        print(x, y)
        points_2D += [(x, y)]

cv2.imshow("square", img_square_u)
cv2.setMouseCallback("square", mouse_event, img_square_u)
cv2.waitKey()
cv2.destroyAllWindows()

points_2D = np.array(points_2D, dtype='double')
print('points_2D:', points_2D)

points_3D = np.array([list(map(float, input().strip().split())) for _ in range(4)], dtype='double')
points_3D = np.concatenate((points_3D, np.zeros((4, 1), dtype='double')), axis=1)
print('points_3D:', points_3D)

dist = np.zeros((4, 1)) # 왜곡보정된 사진을 사용하기 때문에 dist=0으로 둔다
retval, rvec, tvec = cv2.solvePnP(points_3D, points_2D, mtx, dist, rvec=None, tvec=None, useExtrinsicGuess=None, flags=None)
R, _ = cv2.Rodrigues(rvec)
t = tvec

np.save(str(param_dir / 'R'), R)
np.save(str(param_dir / 't'), t)

print(R)
print('\n')
print(t)
