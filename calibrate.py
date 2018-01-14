#! /usr/bin/python
# coding=utf-8

from car import Car
from encoder import Encoder
from sklearn import linear_model
import numpy as np
import time

if __name__ == '__main__':
    car = Car()
    encoder = Encoder()
    encoder.command(1)
    sample_num = 3
    d = np.zeros(sample_num); l = np.zeros(sample_num); r = np.zeros(sample_num);

    for i in range(sample_num):
        car.set_duty_cycle((i+1)*((-1)**i)*30, (i+1)*((-1)**i)*30)
        time.sleep(2)
        left1, right1 = encoder.get_speed()
        time.sleep(1)
        left2, right2 = encoder.get_speed()
        #~ #~
        d[i] = (i+1)*30
        l[i] = int(left1 + left2)/2
        r[i] = int(right1 + right2)/2
        car.set_duty_cycle(0, 0)
        time.sleep(3)

    print("Left speed: " + str(l))
    print("Right speed: " + str(r))
    
    encoder.command(0)
    car.set_duty_cycle(0, 0)
    
    d = d.reshape(-1, 1)
    l = l.reshape(-1, 1)
    r = r.reshape(-1, 1)

    regr = linear_model.LinearRegression()
    regr.fit(d, l)
    coef_left, intercept_left = regr.coef_, regr.intercept_
    regr.fit(d, r)
    coef_right, intercept_right = regr.coef_, regr.intercept_
    
    line=np.array([[coef_left[0][0], intercept_left[0]], [coef_right[0][0], intercept_right[0]]])
    print(line)

    np.savetxt("./settings.txt", line)




