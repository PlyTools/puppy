

import threading
import cv2
import sys
import os
import numpy as np
import math
import matplotlib.pyplot as plt

class NeuralNetwork(object):
    
    def __init__(self):
        self.model = cv2.ml.ANN_MLP_create()

    def create(self):
        layer_size = np.int32([38400, 32, 4])
        self.model.setLayerSizes(layer_size)
        self.model.load('mlp_xml/mlp.xml')

    def predict(self, samples):
        ret, resp = self.model.predict(samples)
        return resp.argmax(-1)

class ObjectDetection(object):
    
    def __init__(self):
        self.red_light = False
        self.green_light = False
        self.yellow_light = False

    def detect(self, cascade_classifier, gray_image, image):

        # y camera coordinate of the target point 'P'
        v = 0

        # minimum value to proceed traffic light state validation
        threshold = 50
        
        # detection
        cascade_obj = cascade_classifier.detectMultiScale(
            gray_image,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
        )

        # draw a rectangle around the objects
        for (x_pos, y_pos, width, height) in cascade_obj:
            cv2.rectangle(image, (x_pos+5, y_pos+5), (x_pos+width-5, y_pos+height-5), (255, 255, 255), 2)
            v = y_pos + height - 5
            #print(x_pos+5, y_pos+5, x_pos+width-5, y_pos+height-5, width, height)

            # stop sign
            if width/height == 1:
                cv2.putText(image, 'STOP', (x_pos, y_pos-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # traffic lights
            else:
                roi = gray_image[y_pos+10:y_pos + height-10, x_pos+10:x_pos + width-10]
                mask = cv2.GaussianBlur(roi, (25, 25), 0)
                (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask)
                
                # check if light is on
                if maxVal - minVal > threshold:
                    cv2.circle(roi, maxLoc, 5, (255, 0, 0), 2)
                    
                    # Red light
                    if 1.0/8*(height-30) < maxLoc[1] < 4.0/8*(height-30):
                        cv2.putText(image, 'Red', (x_pos+5, y_pos-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                        self.red_light = True
                    
                    # Green light
                    elif 5.5/8*(height-30) < maxLoc[1] < height-30:
                        cv2.putText(image, 'Green', (x_pos+5, y_pos - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        self.green_light = True
    
                    # yellow light
                    #elif 4.0/8*(height-30) < maxLoc[1] < 5.5/8*(height-30):
                    #    cv2.putText(image, 'Yellow', (x_pos+5, y_pos - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
                    #    self.yellow_light = True
        return v

if __name__ == "__main__":
    # cascade classifiers
    sensor_data = " "
    stream_bytes = ' '
    stop_flag = False
    stop_sign_active = True
    
    # # create neural network
    # model = NeuralNetwork()
    # model.create()

    stop_cascade = cv2.CascadeClassifier('cascade_xml/stop_sign.xml')
    light_cascade = cv2.CascadeClassifier('cascade_xml/traffic_light.xml')

    od = ObjectDetection()
    image = cv2.imread(os.path.abspath(sys.argv[1]), cv2.IMREAD_COLOR)
    gray = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
    # image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_UNCHANGED)

    # # lower half of the image
    # half_gray = gray[120:240, :]
    
    # object detection
    v_param1 = od.detect(stop_cascade, gray, image)
    v_param2 = od.detect(light_cascade, gray, image)
    print("v_param1: %s, v_param2: %s"%(v_param1, v_param2))
    print("red_light: %s, green_light: %s, yellow_light: %s"%(od.red_light, od.green_light, od.yellow_light))
    


    
    # distance measurement
    if v_param1 > 0 or v_param2 > 0:
        # d1 = d_to_camera.calculate(v_param1, h1, 300, image)
        # d2 = d_to_camera.calculate(v_param2, h2, 100, image)
        # d_stop_sign = d1
        # d_light = d2
        d_stop_sign = 18
        d_light = 18

    plt.imsave('image', image)
    #cv2.imshow('mlp_image', half_gray)

    # # reshape image
    # image_array = half_gray.reshape(1, 38400).astype(np.float32)
    
    # # neural network makes prediction
    # prediction = model.predict(image_array)

    # # stop conditions
    # if sensor_data is not None and sensor_data < 30:
    #     print("Stop, obstacle in front")
    #     # rc_car.stop()
    
    # elif 0 < d_stop_sign < 25 and stop_sign_active:
    #     print("Stop sign ahead")
    #     # rc_car.stop()

    #     # stop for 5 seconds
    #     if stop_flag is False:
    #         stop_start = cv2.getTickCount()
    #         stop_flag = True
    #     stop_finish = cv2.getTickCount()

    #     stop_time = (stop_finish - stop_start)/cv2.getTickFrequency()
    #     print("Stop time: %.2fs" % stop_time)

    #     # 5 seconds later, continue driving
    #     if stop_time > 5:
    #         print("Waited for 5 seconds")
    #         stop_flag = False
    #         stop_sign_active = False

    # elif 0 < d_light < 30:
    if True:
        #print("Traffic light ahead")
        if od.red_light:
            print("Red light")
            # rc_car.stop()
        elif od.green_light:
            print("Green light")
            pass
        elif od.yellow_light:
            print("Yellow light flashing")
            pass
        

    # else:
    #     # rc_car.steer(prediction)
    #     stop_start = cv2.getTickCount()
    #     d_stop_sign = 25

    #     if stop_sign_active is False:
    #         drive_time_after_stop = (stop_start - stop_finish)/cv2.getTickFrequency()
    #         if drive_time_after_stop > 5:
    #             stop_sign_active = True
