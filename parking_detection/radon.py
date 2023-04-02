##
from skimage.transform import radon, rescale, iradon
import cv2
import numpy as np
import matplotlib.pyplot as plt

# path = "C:/Users/sinjy/PycharmProjects/GIGACHA/parking_detection/data/random_img.png"
path = "C:/Users/sinjy/PycharmProjects/GIGACHA/parking_detection/data/parking_line.png"
img = cv2.imread(path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.medianBlur(img, ksize=13)
print(img.shape)
plt.imshow(img, cmap='gray')
plt.show()

##
import time
img = cv2.resize(img, (480, 480))
st = time.time()
rp = radon(img)
irp = iradon(rp)
print(time.time() - st)
plt.imshow(irp, cmap='gray')
plt.show()
