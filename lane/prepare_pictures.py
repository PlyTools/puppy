import urllib.request as request
from lane import settings
from config import config
import numpy as np
import cv2
import os
import time


'''
Prepare:
    In raspberryPi:

    ```
    cd Tools
    bash change_network.sh wifi
    bash remote_camera.sh
    ```
    
    In PC
    ```
    config the raspi_ip in config module
    ```
'''


host = config.raspi_ip + ":8080"  # ip on raspberryPi
hoststr = 'http://' + host + '/?action=stream'

def read_image_from_RPi(hoststr):
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
    img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),flags=1)
    # 左右翻转 + 上下翻转 = 旋转180度
    flipped = cv2.flip(img, -1)
    return flipped

def save_as_calibrate_image(hoststr):
    i = 1
    while 1:
        img = read_image_from_RPi(hoststr)
        cv2.imwrite(os.path.join("calibrate_images", 'cal' + str(i) + ".jpg"), img)
        print("save cal" + str(i) + " successfully")
        # 每3秒变动棋盘图位置
        time.sleep(3)
        i += 1


if __name__ == '__main__':
    save_as_calibrate_image(hoststr)