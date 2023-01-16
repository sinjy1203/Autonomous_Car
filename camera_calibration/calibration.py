## import
import numpy as np
import cv2
import glob
import pickle
import time
from pathlib import Path

## 이미지 크기 & 디렉토리
W, H = 1900, 1090
raw_img_dir = Path('./data/raw_chess')
param_dir = Path('./camera_parameter')
if not param_dir.exists():
    param_dir.mkdir(exist_ok=True)

## reprojection error

def reprojection_error(imgpoints, objpoints, mtx, dist, rvecs, tvecs):
    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        mean_error = mean_error + error

    print("total error: " + str(mean_error/len(objpoints)))
    return mean_error

## termination criteria
wc, hc = 9, 6  # checker board에 안쪽 코너 개수
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

## checker board의 각 코너의 월드좌표계 like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
# 체커보드의 평면을 월드좌표계의 Z=0인 평면으로 가정
objp = np.zeros((wc*hc,3), np.float32)
objp[:,:2] = np.mgrid[0:wc,0:hc].T.reshape(-1,2)

## 100개 이상의 checkerboard image를 이용해 카메라 파라미터 계산
objpoints = [] # 여러개의 이미지에 대한 3d point in real world space
imgpoints = [] # 여러개의 이미지에 대한 2d points in image plane.
img_dirs = glob.glob(str(raw_img_dir / '*.png')) # 저장한 여러 이미지 데이터 디렉토리
print(img_dirs)

for img_dir in img_dirs: # 각 이미지에 대한 camera calibration
    frame = cv2.imread(img_dir)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # checker board를 찾고 코너 좌표반환
    # ret: 패턴 감지 유무, corners: 감지된 코너의 좌표들
    ret, corners = cv2.findChessboardCorners(gray, (wc, hc), None)
    print(ret)

    # 감지할 경우 코너 좌표 개선
    if ret == True:
        objpoints.append(objp)

        # 원본 이미지와 코너 위치를 이용해 원래 위치의 작은 이웃내에서 가장 좋은 코너위치 찾기
        # gray: 이미지, corners: 찾은 코너 위치, criteria: 미세 조정의 반복 프로세스 종료 기준
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        frame = cv2.drawChessboardCorners(frame, (wc,hc), corners2,ret)
        print("chessobard corner detected. curr num objpoints : " + str(len(objpoints)) +  ", curr num imgpoints : " + str(len(imgpoints)))

    # cv2.imshow('res',frame)
    # time.sleep(5)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

print("finish")

## 최종 카메라 파라미터 계산
# mtx: 내부 카메라 파라미터 (3x3), dist: 렌즈 왜곡계수, rvecs & tvecs: 외부 카메라 파라미터(회전 & 이동벡터)
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

error = reprojection_error(imgpoints, objpoints, mtx, dist, rvecs, tvecs)

cv2.destroyAllWindows()

##
print("camera matrix")
print(mtx)
print("distortion coeff")
print(dist)
print("error")
print(error)


# save camera parameters:
with open(param_dir / 'cam_calib.pkl', 'wb') as f:
    pickle.dump([mtx, dist, rvecs, tvecs], f)