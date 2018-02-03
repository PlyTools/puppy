import numpy as np
import cv2

lower_real_red = np.array([120, 100, 50])
upper_real_red = np.array([200, 255, 255])

lower_red = np.array([40, 150, 20])
upper_red = np.array([120, 255, 255])

lower_green = np.array([20, 20, 20])
upper_green = np.array([60, 255, 255])


def masked(image):

    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    red = cv2.bitwise_and(image, image, mask=red_mask)
    green = cv2.bitwise_and(image, image, mask=green_mask)