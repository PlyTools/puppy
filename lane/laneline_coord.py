import cv2
import urllib2
import numpy as np
import sys
import matplotlib.pyplot as plt

from linesearch import *

'''
Prepare:
    In raspberryPi:

    ```
    cd Tools
    bash change_network.sh wifi
    bash remote_camera.sh
    ```

    In laptop computer:
    
    ```
    conda env create -f=environment.yml --name py2 --debug -v -v
    source activate py2
    ```

    Run:

    ```
    python laneline_coord.py
    ```

    (array([  1.36666667e-02,  -2.13888889e+01,   4.20000000e+01, -1.00000000e+00,   1.45800000e+03]), 8.224282026290894)
    (array([  1.36666667e-02,  -2.13888889e+01,   4.20000000e+01,  0.00000000e+00,   1.47100000e+03]), 0.5016670227050781)
    (array([  1.36666667e-02,  -2.13888889e+01,   4.20000000e+01,  0.00000000e+00,   1.47100000e+03]), 0.5490009784698486)
        ...
    (array([  1.36666667e-02,  -2.13888889e+01,   4.20000000e+01,  0.00000000e+00,   1.46900000e+03]), 0.39974021911621094)

    Means:
        Initiate the first image in 8.22 seconds.
        return array([  1.36666667e-02,  -2.13888889e+01,   4.20000000e+01, -1.00000000e+00,   1.45800000e+03])
        a = 1.36e-2
        b = -2.13e1
        c = 4.2e1
        d = -1

        For 2nd, 3rd image, one image were processed in 0.50, 0.55 second and returned a np array respectly.
'''

host = "192.168.1.85:8080"  # ip on raspberryPi
hoststr = 'http://' + host + '/?action=stream'

src = np.array([[
    [0, 350],
    [240,240],
    [400,240],
    [640,350]
]]).astype(np.float32)

dst = np.array([[
    [10,200],
    [10,0],
    [90,0],
    [90,200]
]]).astype(np.float32)
M    = cv2.getPerspectiveTransform(src, dst)

initParams = [
        np.linspace(0.001, 0.02, 10),
        np.array(list(np.linspace(1.5, 50, 10)) + list(np.linspace(-50, 1.5, 10))),
        np.arange( 40, 50, 2),
        np.arange(-15, 15, 2)
]
refPos = [50, 180] # The position of the top-center of chess-board on the ground in img_t
    
def imageReadFromraspberryPi(hoststr):
    stream=urllib2.urlopen(hoststr)
    bytes=''
    while True:
        bytes+=stream.read(1024)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a!=-1 and b!=-1:
            break
        
    jpg = bytes[a:b+2]
    bytes= bytes[b+2:]
    img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),flags=1)
    return img


def perspectTransform(img, M_trans):
    # binarize image for white line
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = (gray<180).astype(np.uint8)*255
    
    # perspectTransform binarized image
    img_t = cv2.warpPerspective(gray, M_trans, (100,200), cv2.WARP_INVERSE_MAP)
    img_t[180:,0:10] = 255
    img_t[180:,90:]  = 255
    return img_t


def processImage(hoststr, M_trans, initParams, refPos):
    seedParams = []
    timePrev = time.time()
    while 1:
        img = imageReadFromraspberryPi(hoststr)
        img_t = perspectTransform(img, M_trans)
        paramSearch = None
        if len(seedParams) == 0:
            paramSearch = initParams
        else:
            lla = np.linspace(seedParams[0]-(initParams[0][1]-initParams[0][0]),
                              seedParams[0]+(initParams[0][1]-initParams[0][0]), 3)
            llb = np.linspace(seedParams[1]-(initParams[1][1]-initParams[1][0]),
                              seedParams[1]+(initParams[1][1]-initParams[1][0]), 3)
            llc = np.arange(seedParams[2]-2, seedParams[2]+3, 2)
            lld = np.arange(seedParams[3]-1, seedParams[3]+2)
            paramSearch = [lla, llb, llc, lld]

        coords,params = getBestParams(img_t, paramSearch, refPos)
        score = params[4]
        if score < 50:
            seedParams = []
        else:
            seedParams = params
        
        timeNow = time.time()
        print(params, timeNow - timePrev)
        timePrev = timeNow

if __name__ == '__main__':
    processImage(hoststr, M, initParams, refPos)