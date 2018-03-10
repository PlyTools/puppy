import cv2
import urllib.request as request
import numpy as np
import sys
import matplotlib.pyplot as plt
import time


host = "183.172.54.178:8080"  # ip on raspberryPi
hoststr = 'http://' + host + '/?action=stream'

def imageReadFromraspberryPi(hoststr):
    stream=request.urlopen(hoststr)
    bytes=b''
    while True:
        bytes += stream.read(1024)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a!=-1 and b!=-1:
            break
        
    jpg = bytes[a:b+2]
    bytes= bytes[b+2:]
    # print(jpg)
    img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),flags=1)
    flipped = cv2.flip(img, -1)
    return flipped

def processImage(hoststr):
    i = 1
    while 1:
        img = imageReadFromraspberryPi(hoststr)
        cv2.imwrite('./calibrateImage/cal' + str(i) +  ".png", img)
        print("cal" + str(i) + " successfully")
        time.sleep(0.5)
        i+=1

if __name__ == '__main__':
    processImage(hoststr)