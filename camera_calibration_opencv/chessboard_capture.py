import cv2
from pathlib import Path
import shutil

W, H = 640, 480

data_dir = Path('./data/raw_chess')
# if data_dir.exists():
#     shutil.rmtree(data_dir)
# data_dir.mkdir(exist_ok=True)

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
print(cap.isOpened())

cap.set(cv2.CAP_PROP_FRAME_WIDTH, W)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, H)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
print(cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

cnt = 0
while True:
    ret, frame = cap.read()
    cv2.imshow("VideoFrame", frame)
    if cv2.waitKey(1) == ord('c'):
        img = cv2.imwrite(str(data_dir / 'chess{}.png').format(cnt), frame)
        cnt += 1
        print('save chess {}'.format(cnt))
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()