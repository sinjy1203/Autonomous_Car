import numpy as np

R = np.load('R.npy')
Z_c = np.array([[0], [0], [1]])
R_inv = np.linalg.inv(R)
Z_w = np.dot(R_inv, Z_c)
theta_pan = np.arctan2(Z_w[2, 0], np.sqrt(Z_w[0, 0]**2 + Z_w[1, 0]**2))
print(theta_pan * 180 / np.pi)