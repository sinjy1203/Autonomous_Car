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

    ########################## ground truth 이부분 수정
    def ground_truth(self, image, patch_pos, mode='mean'):
        x, y, w, h = patch_pos
        image_patch = image[x:x+w, y:y+h]
        if mode == 'mean':
            image_gt = \
                ((image * (image_patch.mean() / image.mean(axis=(0, 1)))).clip(0, 255).astype(int))
        if mode == 'max':
            image_gt = ((image * 1.0 / image_patch.max(axis=(0, 1))).clip(0, 1))

# percentile: 최댓값의 기준(흰색의 기준)을 어떤 것으로 할거냐
# percentile이 낮을 수록 이미지가 전체적으로 흰색이 됨
def white_patch(image, percentile=100):
    white_patch_image = img_as_ubyte((image*1.0 /
                                   np.percentile(image,percentile,
                                   axis=(0, 1))).clip(0, 1))
    return white_patch_image

white_patch(img, 90)