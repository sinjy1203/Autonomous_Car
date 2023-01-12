import cv2

W, H = 1090, 1920

cap = cv2.VideoCapture(1)
print(cap.isOpened())

cap.set(cv2.CAP_PROP_FRAME_WIDTH, W)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, H)
print(cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


while True:
    ret, frame = cap.read()
    cv2.imshow("VideoFrame", frame)
    if cv2.waitKey(1) == ord('c'):
        img = cv2.imwrite('img_capture.png', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()