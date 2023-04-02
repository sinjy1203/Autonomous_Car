import cv2
from pathlib import Path

data_dir = Path('C:/Users/sinjy/PycharmProjects/GIGACHA/parking_detection')
cap = cv2.VideoCapture(str(data_dir / "video_data/output302.avi"))

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        cv2.imshow('frame', frame)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('c'):
        cv2.imwrite(str(data_dir / 'data/parking_line.png'), frame)
        break
cap.release()
cv2.destroyAllWindows()
