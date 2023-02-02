import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread, imshow
from skimage import img_as_ubyte
from matplotlib.patches import Rectangle
from test2 import Homomorphic

class AWB:
    def __init__(self):
        pass
    def white_patch(self, image, percentile=100):
        white_patch_image = img_as_ubyte(
            (image * 1.0 / np.percentile(image, percentile, axis=(0, 1))).
            clip(0, 1))
        return white_patch_image

    def gray_world(self, image):
        image_grayworld = ((image * (image.mean() / image.mean(axis=(0, 1)))).
                           clip(0, 255).astype(int))
        return image_grayworld

    def ground_truth(self, image, patch_pos, mode='mean'):
        x, y, w, h = patch_pos
        image_patch = image[y:y+h, x:x+w]
        if mode == 'mean':
            image_gt = \
                ((image * (image_patch.mean() / image.mean(axis=(0, 1)))).clip(0, 255).astype(int))
        if mode == 'max':
            image_gt = ((image * 1.0 / image_patch.max(axis=(0, 1))).clip(0, 1))

if __name__ == "__main__":
    awb = AWB()
    cap = cv.VideoCapture('C:/GIGACHA_video/traffic_video/output21_.avi')

    while True:
        global pos
        ret, img = cap.read()
        pos = []
        # img_awb = awb.gray_world(img).astype(np.uint8)
        img_ho = Homomorphic(img)
        cv.imshow('original', img)
        cv.imshow('Homomorphic', img_ho)
        if cv.waitKey(20) & 0xFF == ord('q'):
            break

    # cap.release()
    cv.destroyAllWindows()

