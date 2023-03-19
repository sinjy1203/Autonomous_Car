import numpy as np
import matplotlib.pyplot as plt
import cv2
from pathlib import Path

param_dir = Path('camera_param')

cameraParam = np.load(str(param_dir / 'mtx.npy'))
R = np.load(str(param_dir / 'R.npy'))
t = np.load(str(param_dir / 't.npy'))
fx = cameraParam[0, 0]
fy = cameraParam[1, 1]
cx = cameraParam[0, 2]
cy = cameraParam[1, 2]

f = np.array([fx, fy])
c = np.array([cx, cy])
p = np.array([0, 0])

while True:
    p = list(map(float, input().split()))
    p = np.array(p)

    normalized_p = (p - c) / f
    pc = np.concatenate([normalized_p, np.ones((1,))])[:, np.newaxis]

    pw = np.dot(R.T, pc - t)

    Cw = np.dot(R.T, -t)
    k = (0 - Cw[2, 0]) / (pw[2, 0] - Cw[2, 0])
    P = Cw + k * (pw - Cw)
    print(P)
