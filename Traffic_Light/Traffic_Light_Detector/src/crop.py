# coding=utf-8

import cv2

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False


def select(video_file):
    """
    :param str video_file:  
    :rtype: enumerate
    """
    cap = cv2.VideoCapture(video_file)

    def click_and_crop(event, x, y, flags, param):
        # grab references to the global variables
        global refPt, cropping

        # if the left mouse button was clicked, record the starting
        # (x, y) coordinates and indicate that cropping is being
        # performed
        if event == cv2.EVENT_LBUTTONDOWN:
            refPt = [(x, y)]
            cropping = True

        # check to see if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
            # record the ending (x, y) coordinates and indicate that
            # the cropping operation is finished
            refPt.append((x, y))
            cropping = False

            # draw a rectangle around the region of interest
            cv2.rectangle(frame, refPt[0], refPt[1], (0, 255, 0), 2)
            cv2.imshow("frame", frame)

    # We use only first frame
    _, frame = cap.read()

    clone = frame.copy()
    cv2.namedWindow("frame")
    cv2.setMouseCallback("frame", click_and_crop)

    # keep looping until the 'q' key is pressed
    while True:
        # display the image and wait for a keypress
        cv2.imshow("frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the 'r' key is pressed, reset the cropping region
        if key == ord("r"):
            frame = clone.copy()

        # if the 'q' key is pressed, break from the loop
        elif key == ord("q"):
            break

    # if there are two reference points, then crop the region of interest
    # from teh image and display it
    if len(refPt) == 2:
        roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        cv2.imshow("ROI", roi)
        cv2.waitKey(0)

    # close all open windows
    cv2.destroyAllWindows()
    cap.release()

    return "frame={},{},{},{}".format(refPt[0][1], refPt[1][1], refPt[0][0], refPt[1][0])
