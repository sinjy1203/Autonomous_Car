## import
import os
import numpy as np
import cv2
import glob
import pickle
import time
from pathlib import Path
import shutil


def cal_mtx_dist(corner_count=(8, 6), checkerboard_dir='./checkerboards',
                 param_dir='./camera_param'):
    # 저장된 checkerboard images을 통해 camera parameter을 계산하고 저장

    checkerboard_dir = Path(checkerboard_dir)
    param_dir = Path(param_dir)

    wc, hc = corner_count  # checkerboard의 내부 코너 개수
    if not checkerboard_dir.exists():  # checkerboard images들의 저장 디렉토리
        raise Exception('checkerboard images가 없음')
    if not param_dir.exists():  # camera parameter 저장 디렉토리
        param_dir.mkdir(exist_ok=True)

    # checker board의 각 코너의 월드좌표계 like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    # 체커보드의 평면을 월드좌표계의 Z=0인 평면으로 가정
    objp = np.zeros((wc * hc, 3), np.float32)
    objp[:, :2] = np.mgrid[0:wc, 0:hc].T.reshape(-1, 2)

    # checkerboard images를 이용해 카메라 파라미터 계산
    objpoints = []  # 여러개의 이미지에 대한 3d point in real world space
    imgpoints = []  # 여러개의 이미지에 대한 2d points in image plane.
    checkboard_fnames = glob.glob(str(checkerboard_dir / '*.png'))  # 저장한 여러 이미지 데이터 디렉토리

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # cornersubpix의 반복 프로세스 종료기준

    for checkboard_fname in checkboard_fnames:  # 각 이미지에 대한 camera calibration
        checkboard = cv2.imread(checkboard_fname)
        checkboard_gray = cv2.cvtColor(checkboard, cv2.COLOR_BGR2GRAY)

        # checker board를 찾고 코너 좌표반환
        # ret: 패턴 감지 유무, corners: 감지된 코너의 좌표들
        ret, corners = cv2.findChessboardCorners(checkboard_gray, (wc, hc), None)
        print(Path(checkboard_fname).name, ret)

        # 감지할 경우 코너 좌표 개선
        if ret == True:
            objpoints.append(objp)

            # 원본 이미지와 코너 위치를 이용해 원래 위치의 작은 이웃내에서 가장 좋은 코너위치 찾기
            # gray: 이미지, corners: 찾은 코너 위치, criteria: 미세 조정의 반복 프로세스 종료 기준
            corners2 = cv2.cornerSubPix(checkboard_gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            checkboard_corner = cv2.drawChessboardCorners(checkboard, (wc, hc), corners2, ret)
            print("chessobard corner detected. curr num objpoints : " + str(
                len(objpoints)) + ", curr num imgpoints : " + str(len(imgpoints)))

            cv2.imshow('res', checkboard_corner)
            if cv2.waitKey(0) == ord('n'):
                pass

    cv2.destroyAllWindows()
    print("finish calibration")

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, checkboard_gray.shape[::-1], None, None)

    print("camera matrix")
    print(mtx)
    print("distortion coeff")
    print(dist)

    # save camera parameters:
    np.save(str(param_dir / 'mtx'), mtx)
    np.save(str(param_dir / 'dist'), dist)


if __name__ == "__main__":
    cal_mtx_dist()
