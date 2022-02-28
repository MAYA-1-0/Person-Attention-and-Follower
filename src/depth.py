#!/usr/bin/env python3
import cv2
import numpy as np
import pyrealsense2 as rs
import math
import rospy
from std_msgs.msg import Int32
import signal
from threading import Thread

def keyboardInterruptHandler(signal, frame):
	print("interrrupt detected")
	dc.release()
	exit(0)



class VideoGet:
	def __init__(self, src=0):
		self.stream = cv2.VideoCapture(src,cv2.CAP_GSTREAMER)
		(self.grabbed, self.frame) = self.stream.read()
		self.stopped = False

	def start(self):    
		Thread(target=self.get, args=()).start()
		return self

	def get(self):
		while not self.stopped:
			if not self.grabbed:
		        	self.stop()
			else:
		        	(self.grabbed, self.frame) = self.stream.read()

	def stop(self):
		self.stopped = True
		self.stream.release()

class DepthCamera:
	def __init__(self):
		self.pipeline = rs.pipeline()
		config = rs.config()
		pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
		pipeline_profile = config.resolve(pipeline_wrapper)
		device = pipeline_profile.get_device()
		device_product_line = str(device.get_info(rs.camera_info.product_line))
		config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
		config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
		self.pipeline.start(config)

	def get_frame(self):
		frames = self.pipeline.wait_for_frames()
		depth_frame = frames.get_depth_frame()
		color_frame = frames.get_color_frame()
		depth_image = np.asanyarray(depth_frame.get_data())
		color_image = np.asanyarray(color_frame.get_data())
		if not depth_frame or not color_frame:
			return False, None, None
		return True, depth_image, color_image

	def release(self):
		self.pipeline.stop()

dc=DepthCamera()

d=0
w=0
pub = rospy.Publisher("/direction",Int32,queue_size = 1)
face_cascade=cv2.CascadeClassifier("/home/brain/stereo_ws/src/stereo_vision/src/opencv-master/data/haarcascades/haarcascade_frontalface_default.xml")




while True:
	ret, depth_frame, color_frame = dc.get_frame()
	width=color_frame.shape[0]
	height=color_frame.shape[1]
	gray=cv2.cvtColor(color_frame,cv2.COLOR_BGR2GRAY)
	faces=face_cascade.detectMultiScale(gray,1.5,5)
	for x,y,w,h in faces:
        	cv2.rectangle(color_frame,(x,y),(x+w,y+h),(0,255,0),2)
		d=320-(x+(w/2))
      		p = 240-(y+(h/2))	
		cv2.putText(color_frame,"Angle"+str(theta*57.3),(x,y-1),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
      		cv2.imshow("Frame",color_frame)




	signal.signal(signal.SIGINT, keyboardInterruptHandler)

