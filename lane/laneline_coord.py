import cv2
import numpy as np
import sys
import matplotlib.pyplot as plt
sys.path.append("../")
from lane.linesearch import *
from config import config

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

src = np.array([[
    [0, 430],
    [270,300],
    [400,300],
    [640,420]
]]).astype(np.float32)

dst = np.array([[
    [10,200],
    [10,0],
    [90,0],
    [90,200]
]]).astype(np.float32)

M = cv2.getPerspectiveTransform(src, dst)

initParams = [
        np.linspace(0.001, 0.02, 10),
        np.array(list(np.exp(np.linspace(0.5, 3, 8)) + list(np.exp(np.linspace(-3, -0.5, 8))))),
        np.arange( 25, 40, 2),
        np.arange(-15, 15, 2)
]

calibrate = 7

refPos = [50, 180] # The position of the top-center of chess-board on the ground in img_t


def perspectTransform(img, M_trans):
    # binarize image for white line
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = (gray<180).astype(np.uint8)*255
    # perspectTransform binarized image
    img_t = cv2.warpPerspective(gray, M_trans, (100,200), cv2.WARP_INVERSE_MAP)
    img_t[180:,0:10] = 255
    img_t[180:,90:]  = 255
    return img_t


def processImage(img, M_trans, params, refPos):
    timePrev = time.time()
    while True:
        img_t = perspectTransform(img, M_trans)
        paramSearch = None
        img_t = ((img_t < 100)*255).astype(np.uint8)
        if len(params) == 0:
            paramSearch = initParams
        else:
            lla = np.linspace(params[0]-(initParams[0][1]-initParams[0][0]),
                              params[0]+(initParams[0][1]-initParams[0][0]), 3)
            llb = np.linspace(params[1]-(initParams[1][1]-initParams[1][0]),
                              params[1]+(initParams[1][1]-initParams[1][0]), 3)
            llc = np.arange(params[2]-2, params[2]+3, 2)
            lld = np.arange(params[3]-1, params[3]+2)
            paramSearch = [lla, llb, llc, lld]

        coords, new_params = getBestParams(img_t, paramSearch, refPos)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(coords[0], coords[4])
        ax.plot(coords[1], coords[4])
        ax.plot(coords[2], coords[4])
        ax.plot(coords[3], coords[4])
        ax.set_xlim(0,100)
        ax.imshow(img_t, "gray")
        fig.savefig("received.png")
        # new_params[3] = new_params[3] - calibrate
        score = new_params[4]
        if score < 50:
            params = []
        else:
            timeNow = time.time()
            print(new_params, timeNow - timePrev)
            return new_params
    
    