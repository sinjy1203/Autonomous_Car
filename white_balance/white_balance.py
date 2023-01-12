##
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread, imshow
from skimage import img_as_ubyte
from matplotlib.patches import Rectangle

##
dinner = imread('dinner.jpg')
plt.imshow(dinner, cmap='gray')

##
fig, ax = plt.subplots(1,2, figsize=(10,6))
ax[0].imshow(dinner)
ax[0].set_title('Original Image')
dinner_max = (dinner*1.0 / dinner.max(axis=(0,1)))
ax[1].imshow(dinner_max)
ax[1].set_title('Whitebalanced Image')

##
fig, ax = plt.subplots(1,2, figsize=(10,6))
ax[0].imshow(dinner)
ax[0].set_title('Original Image')
dinner_mean = (dinner*1.0 / dinner.mean(axis=(0,1)))
ax[1].imshow(dinner_mean.clip(0, 1))
ax[1].set_title('Whitebalanced Image');

##
def percentile_whitebalance(image, percentile_value):
    fig, ax = plt.subplots(1,2, figsize=(12,6))
    for channel, color in enumerate('rgb'):
        channel_values = image[:,:,channel]
        value = np.percentile(channel_values, percentile_value)
        ax[0].step(np.arange(256),
                   np.bincount(channel_values.flatten(),
                   minlength=256)*1.0 / channel_values.size,
                   c=color)
        ax[0].set_xlim(0, 255)
        ax[0].axvline(value, ls='--', c=color)
        ax[0].text(value-70, .01+.012*channel,
                   "{}_max_value = {}".format(color, value),
                    weight='bold', fontsize=10)
    ax[0].set_xlabel('channel value')
    ax[0].set_ylabel('fraction of pixels');
    ax[0].set_title('Histogram of colors in RGB channels')
    whitebalanced = img_as_ubyte(
            (image*1.0 / np.percentile(image,
             percentile_value, axis=(0, 1))).clip(0, 1))
    ax[1].imshow(whitebalanced);
    ax[1].set_title('Whitebalanced Image')
    return ax

##
percentile_whitebalance(dinner, 97.5)

##
fig, ax = plt.subplots(1,2, figsize=(10,6))
ax[0].imshow(dinner)
ax[0].set_title('Original Image')
dinner_gw = ((dinner * (dinner.mean() / dinner.mean(axis=(0, 1))))
             .clip(0, 255).astype(int))
ax[1].imshow(dinner_gw);
ax[1].set_title('Whitebalanced Image');

##
def whitepatch_balancing(image, from_row, from_column,
                         row_width, column_width):
    fig, ax = plt.subplots(1,2, figsize=(10,5))
    ax[0].imshow(image)
    ax[0].add_patch(Rectangle((from_column, from_row),
                              column_width,
                              row_width,
                              linewidth=3,
                              edgecolor='r', facecolor='none'));
    ax[0].set_title('Original image')
    image_patch = image[from_row:from_row+row_width,
                        from_column:from_column+column_width]
    image_max = (image*1.0 /
                 image_patch.max(axis=(0, 1))).clip(0, 1)
    ax[1].imshow(image_max);
    ax[1].set_title('Whitebalanced Image')
whitepatch_balancing(dinner, 600, 1200, 150, 150)
