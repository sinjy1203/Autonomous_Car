import cv2
import numpy as np
from pathlib import Path
from glob import glob

# drawing_fname = Path('./data/drawing_chess/draw_undistortion.jpg')
# raw_fname = Path("./data/undistortion_chess/undistortion_img.jpg")
input_pattern = Path("./data/raw_chess/*.png")
output_dir = Path("./data/drawing_chess")


def mouse_event(event, x, y, flags, param):
    global pos, cnt, output_path
    if event == cv2.EVENT_FLAG_LBUTTON and cnt == 0:
        pos = (x, y)
        cnt += 1
        print(1)
    elif event == cv2.EVENT_FLAG_LBUTTON and cnt == 1:
        param = cv2.line(param, pos, (x, y), (0, 0, 255), 1)
        cv2.imshow("draw", param)
        cv2.imwrite(str(output_path), param)
        print(2)
        cnt = 0

for input_path in glob(str(input_pattern)):
    cnt = 0
    src = cv2.imread(str(input_path))
    cv2.imshow("draw", src)
    output_path = output_dir / Path(input_path).name
    cv2.setMouseCallback("draw", mouse_event, src)
    cv2.imshow("draw", src)
    key = cv2.waitKey()
    if key == ord('c'):
        continue
    if key == ord('q'):
        break