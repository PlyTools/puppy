# -*- coding: utf-8 -*-
# file: tests.py
# author: JinTian
# time: 21/02/2018 1:23 PM
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
module test entrances
"""
from traffic_sign.ts_detect import TrafficSignDetector
import cv2


def t():
    img = cv2.imread('traffic_sign/ts.jpg')

    ts_detector = TrafficSignDetector()
    ts_detector.get_result(img)


if __name__ == '__main__':
    t()