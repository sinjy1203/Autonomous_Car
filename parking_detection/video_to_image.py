import cv2
from pathlib import Path

video_file = './video_data/output201.mp4'
data_dir = './image_data'
data_dir = Path(data_dir)

cap = cv2.VideoCapture(video_file)  # 동영상 캡처 객체 생성
cnt = 4660
while (True):  # Check Video is Available
    ret, frame = cap.read()  # read by frame (ret=TRUE/FAqLSE)s

    cv2.imshow('Original VIDEO', frame)
    if cnt % 20 == 0:
        img = cv2.imwrite(str(data_dir / 'cross{}.png').format(cnt), frame)
        print('save cross{}.png'.format(cnt))
    cnt += 1

    if cv2.waitKey(20) == ord('q'):  # wait 10ms until user input 'esc'
        break

cap.release()  # release memory
cv2.destroyAllWindows()  # destroy All Window