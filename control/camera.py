# -*- coding: utf-8 -*-
from picamera.array import PiRGBArray
from picamera import PiCamera
import matplotlib.pyplot as plt
import time
import cv2
import io
import numpy as np

class Camera:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 5
        self.camera.vflip = True
        time.sleep(2)

    def getFrameArray(self):
        stream = io.BytesIO()
        self.camera.capture(stream, format="jpeg", use_video_port=True)
        frameArray = np.array(stream.getvalue())
        #~ frameArray = np.fromstring(stream.getvalue(), dtype = np.uint8)
        return frameArray
        
    def getFrame(self):
        frameArray = self.getFrameArray()
        frame = cv2.imdecode(frameArray, 1)
        return frame
        
if __name__ == "__main__":
    camera = Camera()
    frame = camera.getFrame()
    plt.imsave("frame.jpeg", frame)

