import cv2
import sys
from pathlib import Path
import time


# Load Web Camera
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


# cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3) # auto mode
# cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1) # manual mode
cap.set(cv2.CAP_PROP_EXPOSURE, -8) # -1 to -13
if not (cap.isOpened()):
    print("File isn't opend!!")

# Set Video File Property
data_dir = Path('data')
if not data_dir.exists():
    data_dir.mkdir()

w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # width
h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # height

# Load frame and Save it
cnt = 30
while (True):  # Check Video is Available
    ret, frame = cap.read()  # read by frame (ret=TRUE/FALSE)s
    if ret:
        cv2.imshow('img', frame)
        if cv2.waitKey(1) == ord('c'):
            img = cv2.imwrite(str(data_dir / 'cross{}.png').format(cnt), frame)
            cnt += 1
            print('save cross{}.png'.format(cnt))

        if cv2.waitKey(1) == ord('q'):  # wait 10ms until user input 'esc'
            break
    else:
        print("ret is false")
        break

cap.release()  # release memory
cv2.destroyAllWindows()  # destroy All Window