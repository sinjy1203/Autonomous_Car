import cv2

W, H = 1090, 1920

capture = cv2.VideoCapture(1)
print(capture.isOpened())

capture.set(cv2.CAP_PROP_FRAME_WIDTH, W)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, H)

while True:
    ret, frame = capture.read()
    # frame = cv2.flip(frame, 1)
    cv2.imshow("VideoFrame", frame)
    if cv2.waitKey(1) == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()