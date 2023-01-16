## import
import os
import numpy as np
import cv2
import glob
import pickle
import time
from pathlib import Path
import shutil

## calibration module
# save checker board img, camera calibration, undistort webcam, draw line for check distortion
class Cal:
    def __init__(self, frame_shape=(1900, 1090), param_dir='./camera_parameter',
                 checkerboards_dir='./data/raw_checkerboard',
                 undistorted_checkerboards_dir='./data/undistortion_checkerboard'):
        self.W, self.H = frame_shape # img shape
        self.param_dir = Path(param_dir) # camera parameter save dir
        self.checkerboards_dir = Path(checkerboards_dir) # checkerboards img dir
        self.undistorted_checkerboards_dir = Path(undistorted_checkerboards_dir)

    def reprojection_error_(self, imgpoints, objpoints, mtx, dist, rvecs, tvecs):
        mean_error = 0
        for i in range(len(objpoints)):
            imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
            error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
            mean_error = mean_error + error

        print("total error: " + str(mean_error / len(objpoints)))
        return mean_error

    def save_checkerboard(self, device=1):
        # capture checker board image and save

        # checkerboard image save dir
        if self.checkerboards_dir.exists():
            shutil.rmtree(self.checkerboards_dir)
        self.checkerboards_dir.mkdir(exist_ok=True)

        # webcam setting
        cap = cv2.VideoCapture(device)
        print("cap_loading success: ", cap.isOpened())
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.W)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.H)
        print("width: {}, height: {}".format(cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        # c 클릭할 때마다 image capture
        cnt = 0
        while True:
            ret, frame = cap.read()
            cv2.imshow("VideoFrame", frame)
            if cv2.waitKey(1) == ord('c'):
                img = cv2.imwrite(str(self.checkerboards_dir / 'checkboard{}.png').format(cnt), frame)
                cnt += 1
                print('save chess {}'.format(cnt))
            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def camera_calibration(self, corner_count=(9, 6), show_corner=True,
                           param_name='cam_calib.pkl'):
        # 저장된 checkerboard images을 통해 camera parameter을 계산하고 저장

        wc, hc = corner_count # checkerboard의 내부 코너 개수
        if not self.checkerboards_dir: # checkerboard images들의 저장 디렉토리
            raise Exception('checkerboard images가 없음')
        if not self.param_dir.exists(): # camera parameter 저장 디렉토리
            self.param_dir.mkdir(exist_ok=True)

        # checker board의 각 코너의 월드좌표계 like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        # 체커보드의 평면을 월드좌표계의 Z=0인 평면으로 가정
        objp = np.zeros((wc * hc, 3), np.float32)
        objp[:, :2] = np.mgrid[0:wc, 0:hc].T.reshape(-1, 2)

        # checkerboard images를 이용해 카메라 파라미터 계산
        objpoints = []  # 여러개의 이미지에 대한 3d point in real world space
        imgpoints = []  # 여러개의 이미지에 대한 2d points in image plane.
        checkboard_fnames = glob.glob(str(self.checkerboards_dir / '*.png'))  # 저장한 여러 이미지 데이터 디렉토리

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
                if show_corner:
                    checkboard_corner = cv2.drawChessboardCorners(checkboard, (wc, hc), corners2, ret)
                    print("chessobard corner detected. curr num objpoints : " + str(
                        len(objpoints)) + ", curr num imgpoints : " + str(len(imgpoints)))

                    cv2.imshow('res',checkboard_corner)
                    if cv2.waitKey(0) == ord('n'):
                        pass

        print("finish calibration")

        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, checkboard_gray.shape[::-1], None, None)

        error = self.reprojection_error_(imgpoints, objpoints, mtx, dist, rvecs, tvecs)

        print("camera matrix")
        print(mtx)
        print("distortion coeff")
        print(dist)
        print("error")
        print(error)

        # save camera parameters:
        with open(self.param_dir / param_name, 'wb') as f:
            pickle.dump([mtx, dist, rvecs, tvecs], f)

    def get_cameramat_dist_(self, filename):

        f = open(filename, 'rb')
        mat, dist, rvecs, tvecs = pickle.load(f)
        f.close()

        print("camera matrix")
        print(mat)
        print("distortion coeff")
        print(dist)
        return mat, dist

    def undistort_webcam(self, device=1, param_name='cam_calib.pkl'):
        if not self.undistorted_checkerboards_dir.exists():
            self.undistorted_checkerboards_dir.mkdir(exist_ok=True)

        mat, dist = self.get_cameramat_dist_()


if __name__ == "__main__":
    cal = Cal()
    cal.camera_calibration(show_corner=False)
