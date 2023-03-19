import cv2
import numpy as np
from pathlib import Path

def UnDistort(img, mtx, dist, w_h):
    w, h = w_h
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]
    return dst

if __name__ == "__main__":
    param_dir = Path('camera_param')
    mtx, dist = np.load(str(param_dir / 'mtx.npy')), np.load(str(param_dir / 'dist.npy'))
    W, H = 640, 480
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    print(cap.isOpened())

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, H)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    print(cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    cnt = 0
    while True:
        ret, frame = cap.read()
        frame = UnDistort(frame, mtx, dist, (640, 480))
        cv2.imshow("VideoFrame", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()