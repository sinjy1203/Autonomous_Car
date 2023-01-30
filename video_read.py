import cv2
from AutoWhiteBalance import AWB

videoFile = 'video/output4.avi' #read video file
cap = cv2.VideoCapture(videoFile) #load as a VideoCapture class
awb = AWB()

while(cap.isOpened()): #Check Video is Available
	ret, frame = cap.read() #read by frame (ret=TRUE/FALSE)
	# white_balanced = awb.gray_world(frame)
	if ret:
		cv2.imshow('VIDEO', frame)
		# cv2.imshow('awb', white_balanced)
		if cv2.waitKey(10) & 0xFF == ord('q'): #wait 10ms until user input
			break
	else:
		print("ret is false")
		break

cap.release() #release memory
cv2.destroyAllWindows() #destroy All Window