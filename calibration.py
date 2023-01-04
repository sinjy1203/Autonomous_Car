import numpy as np
import cv2
import glob
import pickle
import time

W, H = 1900, 1090

def reprojection_error(imgpoints, objpoints, mtx, dist, rvecs, tvecs):
    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        mean_error = mean_error + error

    print("total error: " + str(mean_error/len(objpoints)))
    return mean_error


# termination criteria
wc, hc = 9, 6  # count-1
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((wc*hc,3), np.float32)
objp[:,:2] = np.mgrid[0:wc,0:hc].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
# img_dirs = glob.glob('./data/raw_chess/*.png')
img_dirs = ['./data/raw_chess/raw.jpg']

for img_dir in img_dirs:
    frame = cv2.imread(img_dir)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (wc,hc),None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        frame = cv2.drawChessboardCorners(frame, (wc,hc), corners2,ret)
        print("chessobard corner detected. curr num objpoints : " + str(len(objpoints)) +  ", curr num imgpoints : " + str(len(imgpoints)))

    cv2.imshow('res',frame)
    time.sleep(5)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)


reprojection_error(imgpoints, objpoints, mtx, dist, rvecs, tvecs)


cv2.destroyAllWindows()


print("camera matrix")
print(mtx)
print("distortion coeff")
print(dist)


# Saving the objects:
with open('cam_calib.pkl', 'wb') as f:
    pickle.dump([mtx, dist, rvecs, tvecs], f)