import cv2
import numpy as np


def equal_histogram(source):
    source_yuv = cv2.cvtColor(source, cv2.COLOR_BGR2YUV)
    # equalize the histogram of the Y channel
    source_yuv[:, :, 0] = cv2.equalizeHist(source_yuv[:, :, 0])
    # convert the YUV image back to RGB format
    return cv2.cvtColor(source_yuv, cv2.COLOR_YUV2BGR)


def mse(image_a, image_b):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((image_a.astype("float") - image_b.astype("float")) ** 2)
    err /= float(image_a.shape[0] * image_a.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err
