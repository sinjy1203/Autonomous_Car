##
import cv2
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
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]),
                             minLineLength=min_line_len,
                             maxLineGap=max_line_gap)
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

path = "C:/Users/sinjy/PycharmProjects/GIGACHA/parking_detection/data/parking_line.png"

img = cv2.imread(path, cv2.IMREAD_COLOR)
img = lane_detect(img)
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()


# video_file = "./kcity_cut.mp4" # 동영상 파일 경로
#
# cap = cv2.VideoCapture(video_file)
#
# while True:
#     ret, img = cap.read()
#     img = lane_detect(img)
#     cv2.imshow('result', img)
#
#     if cv2.waitKey(1) == ord('q'):
#         break
#
# cap.release()                       # 캡쳐 자원 반납
# cv2.destroyAllWindows()

##
# import cv2
# import matplotlib.pyplot as plt
# img = cv2.imread("./parking_detection/data/cross0.png")
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# plt.imshow(gray, cmap='gray')
# plt.show()
#
# ##
# blur = cv2.GaussianBlur(gray, (5, 5), 0)
# plt.imshow(blur, cmap='gray')
# plt.show()
#
# ##
# edges = cv2.Canny(blur)
