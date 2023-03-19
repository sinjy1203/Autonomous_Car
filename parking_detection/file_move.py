##
from glob import glob
import shutil
from pathlib import Path
import sys
from tqdm import tqdm

src_dir = Path("C:/Users/sinjy/PycharmProjects/GIGACHA/parking_detection/image_data")
dst_img_dir = Path("C:/Users/sinjy/PycharmProjects/GIGACHA/yolov5/parking/images")
dst_label_dir = Path("C:/Users/sinjy/PycharmProjects/GIGACHA/yolov5/parking/labels")

for path in tqdm(glob(str(src_dir / '*.txt'))):
    path = Path(path)
    if path.name == 'classes.txt':
        continue
    shutil.move(str(path), str(dst_label_dir / path.name))
    img_path = Path(str(path).replace('txt', 'png'))
    shutil.move(str(img_path), str(dst_img_dir / img_path.name))

##
# print(len(glob(str(dst_label_dir / '*'))))
