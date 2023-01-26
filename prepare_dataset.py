## import
import os
from glob import glob
from pathlib import Path
import shutil
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tqdm

## data dir
data_dir = Path('C:/Traffic_Light/01 Traffic light (Sample)')

image_dirs = glob(str(data_dir / '*/*/*.jpg'))
label_dirs = glob(str(data_dir / '*/*/*.txt'))

## label class 개수 파악
# label_dirs = glob('C:/Traffic_Light/labels/*.txt') # => line[0]
label_dirs = glob(str(data_dir / '*/*/*.txt')) # => line[-1]
labels = []
for label_dir in label_dirs:
    with open(label_dir, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = list(map(float, line.strip().split()))
            labels += [line[-1]]
labels_series = pd.Series(labels)
print(labels_series.value_counts())

## 데이터셋 label to yolo format label
def yololabel_format(lst):
    label = class2idx[lst[-1]]
    x, y = (lst[0] + lst[2]) / 2 / 2048, (lst[1] + lst[3]) / 2 / 1536
    w, h = (lst[2] - lst[0]) / 2048, (lst[3] - lst[1]) / 1536
    ans = [label, x, y, w, h]
    ans = ' '.join(list(map(str, ans)))
    return ans

## 1400, 1401, 1403 class인 이미지만 이동하고 label.txt도 yolo 형식으로 변환
des_img = 'C:/Traffic_Light/images'
des_label = 'C:/Traffic_Light/labels'
if os.path.exists(des_img):
    shutil.rmtree(des_img)
    os.mkdir(des_img)
if os.path.exists(des_label):
    shutil.rmtree(des_label)
    os.mkdir(des_label)

target_class = [1400, 1401, 1403] # straight, stop, left
class2idx = {target: i for i, target in enumerate(target_class)}

for label_dir in tqdm.tqdm(label_dirs):
    labels = []
    with open(label_dir, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = list(map(float, line.strip().split()))
            if line[-1] not in target_class:
                continue
            # print(1)
            labels += [yololabel_format(line)]
    if labels:
        image_dir = label_dir[:-4].replace('labels_class_5', 'JPEGImages_mosaic') + '.jpg'
        shutil.copyfile(image_dir, os.path.join(des_img, os.path.basename(image_dir)))

        with open(os.path.join(des_label, os.path.basename(label_dir)), 'w') as f:
            # print(labels)
            for label in labels:
                f.write(label + '\n')

# ## labelimg로 만든 label
# with open("C:/traffic/data/labels/00031695.txt", 'r') as f:
#     lines = f.readlines()
#     for line in lines:
#         line1 = list(map(float, line.strip().split()))
#
# ## 데이터셋에 잇는 label
# with open("C:/Users/011/Downloads/신호등/00031695.txt", 'r') as f:
#     lines = f.readlines()
#     for line in lines:
#         line2 = list(map(float, line.strip().split()))

## 새로운 image랑 label 경로
img_dir = 'C:/Traffic_Light/images'
img_list = glob(img_dir + '/*.jpg')
print(len(img_list))

## train test split
from sklearn.model_selection import train_test_split
train_img_list, val_img_list = train_test_split(img_list, test_size=0.1, random_state=2000)
print(len(train_img_list), len(val_img_list))

## train test 경로저장 파일
data_dir = Path('C:/Traffic_Light')
with open(data_dir / 'train.txt', 'w') as f:
    f.write('\n'.join(train_img_list) + '\n')

with open(data_dir / 'val.txt', 'w') as f:
    f.write('\n'.join(val_img_list) + '\n')

## data.yaml 편집
import yaml

with open(data_dir / 'data.yaml', 'r') as f:
    data = yaml.safe_load(f)

print(data)

data['train'] = str(data_dir / 'train.txt')
data['val'] = str(data_dir / 'val.txt')

with open(data_dir / 'data.yaml', 'w') as f:
  yaml.dump(data, f)

print(data)
