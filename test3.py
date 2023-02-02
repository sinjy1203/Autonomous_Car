import cv2

# Open Pi Camera
# cap = cv2.VideoCapture(1)
# # Set auto exposure to false
# cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)

cap = cv2.VideoCapture(1)
# cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3) # auto mode
# cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1) # manual mode
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_EXPOSURE, -11)
# print(cap.get(cv2.CAP_PROP_EXPOSURE))

while True:
    ret, img = cap.read()
    cv2.imshow('ord', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()