import numpy as np
import cv2
import glob
import pickle
from pathlib import Path

W, H = 1900, 1090

undistortion_dir = Path("./data/undistortion_chess")

def get_cameramat_dist(filename):

    f = open(filename, 'rb')
    mat, dist, rvecs, tvecs = pickle.load(f)
    f.close()

    print("camera matrix")
    print(mat)
    print("distortion coeff")
    print(dist)
    return mat,dist


mat, dist = get_cameramat_dist("cam_calib.pkl")

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, W)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, H)

ret, frame = cap.read()

h,  w = frame.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mat,dist,(w,h),1,(w,h))

cnt = 0
while True:
    ret, frame = cap.read()
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # undistort
    mapx,mapy = cv2.initUndistortRectifyMap(mat,dist,None,newcameramtx,(w,h),5)
    res = cv2.remap(frame,mapx,mapy,cv2.INTER_LINEAR)

    # crop the image
    x,y,w,h = roi
    # res = res[y:y+h, x:x+w]

    cv2.imshow('res',res)
    if cv2.waitKey(1) == ord('c'):
        img = cv2.imwrite(str(undistortion_dir / 'undistortion_capture{}.png').format(cnt), res)
        cnt += 1
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()