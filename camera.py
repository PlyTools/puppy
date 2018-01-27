from picamera.array import PiRGBArray
from picamera import PiCamera
import matplotlib.pyplot as plt
import time
import cv2

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    output_file = "./output_image.jpg"
    plt.imsave(output_file, image)
    break

