#coding=utf-8
from camera.array import PiRGBArray
from picamera import PiCamera
import picamera
import matplotlib.pyplot as plt
import time
import cv2
import io
from lane_lines import annotate_image_array
from car import Car
import sys
import threading
from time import ctime,sleep

threads = []
t1 = threading.Thread(target=Car,)
threads.append(t1)
t2 = threading.Thread(target=camera,)
threads.append(t2)

if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    print ("all over %s" %ctime)
'''
with picamera.PiCamera() as camera:
    #camera.start_preview()
    camera.resolution = (640, 480)
    time.sleep(0.5)
    idx = 0
    with picamera.array.PiRGBArray(camera) as stream:
        while 1:
            print(idx)
            camera.capture(stream, format='bgr')
            # At this point the image is available as stream.array
            image = stream.array
            image = cv2.resize(image, (128,96))
            output_file = "./testFigures2/output_image.%d.%d.jpg" % ( int(time.time()), idx)
            idx += 1
            plt.imsave(output_file, image)
            stream.truncate(0)


            #forward_left = int(sys.argv[1])
            #forward_right = int(sys.argv[2])
            #car.set_speed(forward_left, forward_right)
'''
except KeyboardInterrupt:
    car.__del__()

right_lines_x.append(x2)
