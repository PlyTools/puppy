# coding=utf-8

import cv2
import pandas
import numpy as np
from src.lib import tools
from sklearn.cluster import KMeans


class Calibration(object):

    __norm_frame = None
    __min_median_brightness = None
    __debug_mode = False
    __light_cycle = 1000
    __min_contour_area = 150
    __vertical_positions = []

    def __init__(self, light_cycle, min_contour_area, debug=False):
        self.__norm_frame = None
        self.__min_median_brightness = None
        self.__debug_mode = debug
        self.__light_cycle = light_cycle
        self.__min_contour_area = min_contour_area

    def zeroing_color_calibration(self):
        self.__norm_frame = None
        self.__min_median_brightness = None

    def zeroing_position_calibration(self):
        self.__vertical_positions = []

    def calibrate_traffic_colors(self, image, frame_num):
        """
        :param mat image:  
        :param int frame_num:    
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 220, 240, cv2.THRESH_BINARY)[1]
        median_brightness = (thresh > 0).sum()

        if (self.__min_median_brightness is None) or (median_brightness < self.__min_median_brightness):
            self.__min_median_brightness = median_brightness
            self.__norm_frame = gray

        cv2.putText(image, "Calibrating... Frame {}".format(frame_num), (2, 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.3, (0, 0, 255), 1)
        cv2.putText(image, "Median brightness {}".format(median_brightness), (2, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    0.3, (0, 0, 255), 1)

        norm_frame = None if self.__light_cycle > frame_num else self.__norm_frame

        if self.__debug_mode:
            return norm_frame, tools.concat_hor((image, thresh))
        else:
            return norm_frame, image

    def calibrate_vertical_traffic_position(self, image, frame_num):
        """
        :param mat image:  
        :param int frame_num:    
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        frame_delta = cv2.absdiff(self.__norm_frame, gray)
        thresh = cv2.threshold(frame_delta, 200, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        _, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < self.__min_contour_area:
                continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            self.__vertical_positions.append((y + h) / 2)
            if self.__debug_mode:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.putText(image, "Calibrating... Frame {}".format(frame_num), (2, 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.3, (0, 0, 255), 1)

        positions = None
        if self.__light_cycle < frame_num and len(self.__vertical_positions) > 2:
            # Detect Cluster centers
            positions_array = pandas.DataFrame(self.__vertical_positions)
            kmeans = KMeans(n_clusters=3, init='k-means++', random_state=241)
            labels = kmeans.fit_predict(positions_array)
            positions_array['cluster'] = labels
            means = positions_array.groupby('cluster').mean().values
            # medians = proceed_vertical_positions.groupby('cluster').median().values
            self.__vertical_positions = sorted([item for sublist in means for item in sublist])
            positions = sorted(self.__vertical_positions)

        if self.__debug_mode:
            return positions, tools.concat_hor((image, self.__norm_frame, frame_delta, thresh))
        else:
            return positions, image
