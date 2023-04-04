##
import cv2
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

rho = 1
theta = np.pi / 180
threshold = 90
min_line_len = 30
max_line_gap = 60

##
def gray_blur_edges(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # blur_gray = cv2.GaussianBlur(gray, (5, 5), 0)
    blur_gray = cv2.medianBlur(gray, ksize=13)
    edges = cv2.Canny(blur_gray, 53, 122)
    return edges

##
def region_masking(img):
    mask = np.zeros_like(img)
    img_shape = img.shape
    ignore_mask_color = 255
    vertices = np.array([[0, img_shape[0]/2], [img_shape[1], img_shape[0]/2],
                [img_shape[1], img_shape[0]], [0, img_shape[0]]], np.int32)
    cv2.fillPoly(mask, [vertices], ignore_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

##
def draw_lines(img, lines, color=[255, 0, 0], thickness=5):
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    # lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]),
    #                          minLineLength=min_line_len,
    #                          maxLineGap=max_line_gap)
    lines = cv2.HoughLinesP(img, rho, theta, threshold, maxLineGap=max_line_gap)
    print(len(lines))
    # line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    # draw_lines(line_img, lines)
    # return line_img
    return lines

def lane_detect(img):
    # lines = hough_lines(region_masking(gray_blur_edges(img)), rho, theta, threshold, min_line_len, max_line_gap)
    lines = hough_lines(gray_blur_edges(img), rho, theta, threshold, min_line_len, max_line_gap)

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 0], dtype=np.uint8)
    upper_white = np.array([0, 0, 255], dtype=np.uint8)
    for line in lines:
        x1, y1, x2, y2 = line[0]

        mask = cv2.inRange(img_hsv, lower_white, upper_white)
        ratio = np.sum(mask) / (img.shape[0] * img.shape[1])

        # if ratio > 0.3:
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    return img

# path = "C:/Users/sinjy/PycharmProjects/GIGACHA/parking_detection/data/parking_line.png"
data_dir = Path("C:/Users/sinjy/PycharmProjects/GIGACHA/parking_detection")
cap = cv2.VideoCapture(str(data_dir / "video_data/output302.avi"))

w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS) # 카메라에 따라 값이 정상적, 비정상적

# fourcc 값 받아오기, *는 문자를 풀어쓰는 방식, *'DIVX' == 'D', 'I', 'V', 'X'
fourcc = cv2.VideoWriter_fourcc(*'DIVX')

# 1프레임과 다음 프레임 사이의 간격 설정
delay = round(1000/fps)

# 웹캠으로 찰영한 영상을 저장하기
# cv2.VideoWriter 객체 생성, 기존에 받아온 속성값 입력
out = cv2.VideoWriter(str(data_dir / 'video_data/line_detection.avi'), fourcc, fps, (w, h))

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        lanes = lane_detect(frame)
        cv2.imshow('lanes', lanes)
        out.write(lanes)
        # cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('c'):
        cv2.imwrite(str(data_dir / 'data/parking_line.png'), frame)
        break
out.release()
cap.release()
cv2.destroyAllWindows()

# img = cv2.imread(path, cv2.IMREAD_COLOR)
# # img = lane_detect(img)
# img = gray_blur_edges(img)
# cv2.imshow('img', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

