# coding=utf-8

import cv2

import numpy as np
from src.lib import tools
from src.lib import image_tools
from calibrating import Calibration

statuses = {
        0: 'Red',
        1: 'Yellow',
        2: 'Green'
    }

statuses_colors = {
        0: (0, 0, 255),
        1: (0, 255, 255),
        2: (0, 255, 0)
    }

statuses_visualisation_y = {
        0: 500,
        1: 750,
        2: 500
    }

current_status = None


def detect_vertical2(image, norm_frame):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # detect circles in the image
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)
    # ensure at least some circles were found
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")

        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(image, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

    return tools.concat_hor((image, norm_frame))


def detect_vertical(image, frame, norm_frame, min_contour_area, vertical_positions):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    frame_delta = cv2.absdiff(norm_frame, gray)
    thresh = cv2.threshold(frame_delta, 200, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    _, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < min_contour_area:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)

        current_status = (np.abs(np.asarray(vertical_positions)-(y + h) / 2)).argmin()
        cv2.putText(frame, statuses[current_status], (450, statuses_visualisation_y[current_status]),
                    cv2.FONT_HERSHEY_SIMPLEX, 10, statuses_colors[current_status], 20)

        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return tools.concat_hor((image, norm_frame, frame_delta, thresh))


def given_image(frame, source_crop_frame):
    # if current_status is not None:
    #    cv2.putText(frame, statuses[current_status], (450, statuses_visualisation_y[current_status]),
    #                cv2.FONT_HERSHEY_SIMPLEX, 10, statuses_colors[current_status], 20)
    return tools.concat_hor((cv2.resize(frame, (0,0), fx=0.2, fy=0.2), source_crop_frame))


def run(video_file, frame_crop, light_cycle, min_contour_area, vertical):
    """
    :param str video_file: 
    :param Union[List[str]] frame_crop: 
    :param int light_cycle: 
    :param int min_contour_area: 
    :param bool vertical: 
    """
    cap = cv2.VideoCapture(video_file)

    cv2.namedWindow('traffic_light')
    cv2.setWindowProperty("traffic_light", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    frame_num = 0

    # bg1 = cv2.bgsegm.createBackgroundSubtractorGMG()
    bg1 = cv2.createBackgroundSubtractorMOG2(300, 16, True)
    bg2 = cv2.createBackgroundSubtractorMOG2(300, 200, True)
    bg3 = cv2.bgsegm.createBackgroundSubtractorMOG(history=3000, nmixtures=400, backgroundRatio=0.8, noiseSigma=80)

    while cap.isOpened():

        # calibrate camera
        # frame_num, norm_frame, positions = calibrate(cap, frame_crop, frame_num, light_cycle, min_contour_area) <--- !

        _, frame = cap.read()

        if frame is None:  # Repeat
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        crop_frame = crop(frame, frame_crop)
        gray = cv2.cvtColor(crop_frame, cv2.COLOR_BGR2GRAY)

        # res = tools.concat_hor((bg1.apply(crop_frame, learningRate=1.0/30)))
        res = tools.concat_hor((crop_frame, gray, bg1.apply(gray), bg2.apply(gray), bg3.apply(gray)))

        # res = detect_vertical(crop_frame, frame, norm_frame, min_contour_area, positions) <--- !!!
        # res = detect_vertical(crop_frame, frame, norm_frame, min_contour_area, positions)

        display_frame(cap, crop_frame, frame, res)


def crop(frame, frame_crop):
    crop_frame = frame[int(frame_crop[0]):int(frame_crop[1]), int(frame_crop[2]):int(frame_crop[3])]
    crop_frame = image_tools.equal_histogram(crop_frame)
    return crop_frame


def calibrate(cap, frame_crop, frame_num, light_cycle, min_contour_area):
    # initialize the norm frame in the video stream
    norm_frame = None
    positions = None

    color_calibration_started = False
    position_calibration_started = False
    colors_calibrated = False
    position_calibrated = False
    calibration = Calibration(light_cycle, min_contour_area, True)

    while not colors_calibrated or not position_calibrated:
        _, frame = cap.read()

        crop_frame = crop(frame, frame_crop)

        res = None

        if not colors_calibrated:

            if not color_calibration_started:
                calibration.zeroing_color_calibration()
                color_calibration_started = True
                frame_num = 0
            else:
                frame_num += 1

            norm_frame, res = calibration.calibrate_traffic_colors(crop_frame, frame_num)
            if norm_frame is not None:
                color_calibration_started = False
                colors_calibrated = True

        if colors_calibrated and not position_calibrated:

            if not position_calibration_started:
                calibration.zeroing_position_calibration()
                position_calibration_started = True
                frame_num = 0
            else:
                frame_num += 1

            positions, res = calibration.calibrate_vertical_traffic_position(crop_frame, frame_num)  # if vertical
            if positions is not None:
                position_calibration_started = False
                position_calibrated = True

        display_frame(cap, crop_frame, frame, res)
    return frame_num, norm_frame, positions


def display_frame(cap, crop_frame, frame, res):
    concat_image = tools.concat_ver((given_image(frame, crop_frame), res))
    cv2.imshow('traffic_light', cv2.resize(concat_image, (0, 0), fx=2, fy=2))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        cap.release()
        exit()




