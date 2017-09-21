import numpy as np
import win32api
import win32con
import time
import cv2

VK_CODE = { 'backspace':0x08,
			'left_arrow':0x25,
			'a':0x41,
			'w':0x57,
			's':0x53,
			'd':0x44,
			'right_arrow':0x27,
			'down_arrow':0x28,
			'F5':0x74,
			'esc':0x1B }

def press(args):
    #one press, one release.
	win32api.keybd_event(VK_CODE[args], 0,0,0)
	time.sleep(0.5)
	win32api.keybd_event(VK_CODE[args],0 ,win32con.KEYEVENTF_KEYUP ,0)

		
def denoise(frame):
	frame = cv2.medianBlur(frame,5)
	frame = cv2.GaussianBlur(frame,(15,15),0)
	return frame


cam = cv2.VideoCapture(0)

hand2_cascade = cv2.CascadeClassifier('C:/Users/vanda/Desktop/pytn/project/palm.xml')


while (1):
	
	# Capture frames from the camera
	ret,frame = cam.read()

	# If the frame was properly read.
	if ret is True:
		# lower noise
		frame=denoise(frame)
		
		# get gray img
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		
		# detecting fist and palm by HAAR cascade

		palm = hand2_cascade.detectMultiScale(gray, 1.1, 5)
		
		# just drawing rectangles 
		cv2.rectangle(frame,(0,0),(220,240),(0,150,0),2)
		cv2.rectangle(frame,(220,0),(440,240),(0,150,0),2)
		cv2.rectangle(frame,(0,240),(220,480),(0,150,0),2)
		cv2.rectangle(frame,(220,240),(440,480),(0,150,0),2)
		
		for (x,y,w,h) in palm:
			cv2.rectangle(frame,(x,y),(x+w,y+h),(200,0,0),2)
			if x<220 and y<240:
				press('d')
			if x>220 and y<240:
				press('a')
			if x<220 and y>240:
				press('w')
		cv2.imshow('img',frame)
		key = cv2.waitKey(10) & 0xFF

	if key == 27:
		break

cam.release()
cv2.destroyAllWindows()