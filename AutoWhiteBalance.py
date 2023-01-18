import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread, imshow
from skimage import img_as_ubyte
from matplotlib.patches import Rectangle

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

def mouse_event(event, x, y, flags, param):
    global pos
    if event == cv.EVENT_FLAG_LBUTTON:
        pos += [(x, y)]

if __name__ == "__main__":
    awb = AWB()
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 440)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 440)
    W = cap.get(cv.CAP_PROP_FRAME_WIDTH)
    H = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
    print(W, H)

    while True:
        global pos
        ret, img = cap.read()
        # img_white_patch = awb.white_patch(img)
        # img_gray_world = awb.gray_world(img)
        pos = []
        # img_ground_truth = awb.ground_truth(img, )
        # final = np.hstack((img, img_white_patch, img_gray_world))
        cv.imshow('AWB', img)
        cv.setMouseCallback("AWB", mouse_event, img)
        print(pos)
        # print(final.shape)
        # final = final.astype(np.uint8)
        # cv.imshow('AWB', img)
        if cv.waitKey(20) & 0xFF == ord('q'):
            break

    # cap.release()
    cv.destroyAllWindows()

