import os
import sys
import argparse

import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.externals import joblib


class FrameProcessor():
    '''
    detect traffic light in a frame
    '''
    def __init__(self):
        self.RELEVANT_IMAGE_PART = (0, 180)

    def concat_hor(imgs):
        m = 0
        s = 0
        bs = 1
        for img in imgs:
            m = max(m, img.shape[0])
            s += img.shape[1]+2*bs

        image = np.zeros((m+2*bs, s, 3))

        x = 0
        for img in imgs:
            if len(img.shape) == 3:
                imgg = cv2.copyMakeBorder(img.copy(), bs, bs, bs, bs,
                                          cv2.BORDER_CONSTANT, value=(0, 0, 0))
                image[0:imgg.shape[0], x:x+imgg.shape[1], :] = imgg
            else:
                imgg = cv2.copyMakeBorder(cv2.cvtColor(img, cv2.COLOR_GRAY2BGR),
                                          bs, bs, bs, bs, cv2.BORDER_CONSTANT, value=(0, 0, 0))
                image[0:imgg.shape[0], x:x+imgg.shape[1], :] = imgg
            x += img.shape[1]+2*bs

        return np.asarray(image, dtype=np.uint8)

    def traffic_lights_in_frame(self, image):
        orig = image.copy()
        # convert it to gray scale by cv2.COLOR_BGR2GRAY
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        plt.imsave("gray", gray)
        # convert it to hsv scale by cv2.COLOR_RGB2HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        plt.imsave("hsv", hsv)

        # apply a Gaussian blur to the image then find the brightest region
        radius = 41
        gray = cv2.GaussianBlur(gray, (radius, radius), 0)
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
        brightest = orig.copy()
        cv2.circle(brightest, maxLoc, radius, (255, 0, 0), 2)
        plt.imsave("brightest", brightest)



        # lower_real_red = np.array([120, 100, 50])
        # upper_real_red = np.array([200, 255, 255])
        #
        # lower_red = np.array([40, 150, 20])
        # upper_red = np.array([120, 255, 255])
        #
        # lower_green = np.array([20, 20, 20])
        # upper_green = np.array([60, 255, 255])

        # red_mask = cv2.inRange(hsv, lower_red, upper_red)
        # green_mask = cv2.inRange(hsv, lower_green, upper_green)
        # plt.imsave("red_mask", red_mask)
        # plt.imsave("green_mask", green_mask)
        #
        # red = cv2.bitwise_and(image, image, mask=red_mask)
        # green = cv2.bitwise_and(image, image, mask=green_mask)
        # plt.imsave("red", red)
        # plt.imsave("green", green)
        #
        # circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 0.3, 100)
        # # plt.imsave("circles", circles)
        # # ensure at least some circles were found
        # if circles is not None:
        #     # convert the (x, y) coordinates and radius of the circles to integers
        #     circles = np.round(circles[0, :]).astype("int")
        #
        #     # loop over the (x, y) coordinates and radius of the circles
        #     for (x, y, r) in circles:
        #         # draw the circle in the output image, then draw a rectangle
        #         # corresponding to the center of the circle
        #         cv2.circle(image, (x, y), r, (0, 255, 0), 4)
        #         cv2.rectangle(image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        #
        # plt.imsave("circles", image)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Traffic light detection and localization (Currently only HORIZONTAL RED lights)\n")
    file_type_choices = ["image", "video"]
    parser.add_argument("file_type", type=str, choices=file_type_choices,
                    help="Specify what kind of file you want to process")
    parser.add_argument("file_path", type=str, help="Path to file to be processed")
    args = parser.parse_args()
    frame_processor = FrameProcessor()

    if args.file_type == file_type_choices[1]:
        cap = cv2.VideoCapture(os.path.abspath(args.file_path))
        while cap.isOpened():
            # Capture frame-by-frame
            ret, img = cap.read()

            if ret:
                result = frame_processor.traffic_lights_in_frame(img)
                plt.imsave("Result.png", result)
                # cv2.imshow("Result", result)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    elif args.file_type == file_type_choices[0]:
        img = cv2.imread(os.path.abspath(args.file_path), cv2.IMREAD_COLOR)

        frame_processor.SHOW_LIGHT_COUNT_THRESHOLD = 0
        # Specify part of image to search in
        frame_processor.RELEVANT_IMAGE_PART = (0, img.shape[0])

        result = frame_processor.traffic_lights_in_frame(img)
        # plt.imsave("Result.png", result)
