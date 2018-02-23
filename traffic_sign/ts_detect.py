# -*- coding: utf-8 -*-
# file: ts_detect.py
# author: JinTian
# time: 21/02/2018 1:12 PM
# Copyright 2018 JinTian. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------
"""
this file will do traffic detect using simple image process methods
due to the limitation of compute ability on raspberrypi.
to call this using:

ts_detector = TrafficSignDetector()
ts_detector.get_result(frame_image)

and will return a 2-D list [[sign_cls, x1, y1, x2, y2],
                        [sign_cls, x1, y1, x2, y2],
                        ... ]

beware the current implementation can only process location,
the classification of sign will be added in later.
"""
import cv2
import numpy as np


class TrafficSignDetector(object):

    def __init__(self):
        self.current_frame = None

    def get_result(self, frame):
        self.current_frame = frame
        self.get_location()

    def get_location(self):
        img = self.current_frame
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        blue_lower = np.array([100, 50, 50])
        blue_upper = np.array([124, 255, 255])
        mask = cv2.inRange(hsv, blue_lower, blue_upper)
        print('mask', type(mask), mask.shape)

        blurred = cv2.blur(mask, (9, 9))
        ret, binary = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
        closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        erode = cv2.erode(closed, None, iterations=4)
        dilate = cv2.dilate(erode, None, iterations=4)

        image, contours, hierarchy = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        i = 0
        res = img.copy()
        for con in contours:
            rect = cv2.minAreaRect(con)
            # 矩形转换为box
            box = np.int0(cv2.boxPoints(rect))
            cv2.drawContours(res, [box], -1, (0, 0, 255), 2)
            h1 = max([box][0][0][1], [box][0][1][1], [box][0][2][1], [box][0][3][1])
            h2 = min([box][0][0][1], [box][0][1][1], [box][0][2][1], [box][0][3][1])
            l1 = max([box][0][0][0], [box][0][1][0], [box][0][2][0], [box][0][3][0])
            l2 = min([box][0][0][0], [box][0][1][0], [box][0][2][0], [box][0][3][0])
            print('h1', h1)
            print('h2', h2)
            print('l1', l1)
            print('l2', l2)
            if h1 - h2 > 0 and l1 - l2 > 0:
                # 裁剪矩形区域
                temp = img[h2:h1, l2:l1]
                i += 1
        cv2.imshow('res', res)
        cv2.waitKey(0)

