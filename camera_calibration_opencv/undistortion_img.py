import numpy as np
import cv2
import glob
import pickle
from pathlib import Path

undistortion_dir = Path("./data/undistortion_chess")
raw_img_dir = './data/raw_chess/raw.jpg'

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

img = cv2.imread(raw_img_dir)
h,  w = img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mat,dist,(w,h),0,(w,h))

cnt = 0

# undistort
mapx,mapy = cv2.initUndistortRectifyMap(mat,dist,None,newcameramtx,(w,h),5)
res = cv2.remap(img,mapx,mapy,cv2.INTER_LINEAR)

# crop the image
x,y,w,h = roi
# res = res[y:y+h, x:x+w]

cv2.imshow('res',res)
cv2.imwrite(str(undistortion_dir / 'undistortion_img.jpg').format(cnt), res)

cv2.waitKey()