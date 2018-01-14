#coding:utf-8
import time
import multiprocessing as mp

from pid import PID 
from car import Car
from encoder import Encoder
from camera_collectFiguresOnGrounds import camera_main2
from infrad import Infrad
from ultrasonic import ul_main
# fullL
# fullR
# halfL
# halfR
#TODO all the constants
min_angle = -200
max_angle = 2
kp, ki, kd = [-10, 0, 0]
sample_time = 0.02
left_v = 30
pwm_hz = 50
wheelbase = 12  

def main():
    min_angle = -200
    max_angle = 2
    kp, ki, kd = [-10, 0, 0]
    sample_time = 0.2
    left_v = 30
    pwm_hz = 50
    car = Car()
    sample_time = 1.0 / pwm_hz
    
    # pid = PID(kp, ki, kd, mn=min_angle, mx=max_angle)
    
    share_obj = mp.Value('i', 0)
    obj_b = mp.Value('i', 0)
    p_camera = mp.Process(target=camera_main2, args=(share_obj, obj_b))
    p_camera.start()
    
    share_ul_obj = mp.Value('d', 1000.0)
    p_ul = mp.Process(target=ul_main, args=(share_ul_obj, obj_b))
    p_ul.start()

    inf = Infrad()
    v = 180
    stopSignals = 0
    obstacle_stop_time = 0
    detect_sleep_time = 0
    is_detect = True
    while True:
        # target_angular = camera.get_angel()  #TODO
        # current_angular = get_car_angular() #TODO
        # cte = target_angular - current_angular
        if time.time() - detect_sleep_time > 5:
            is_detect = True
        if share_ul_obj.value < 40:
            if is_detect == False:
                t = time.time() - detect_sleep_time
                if t > 5:
                    is_detect = True
            if time.time() - obstacle_stop_time > 2:
                cnt = 0
                left_v *= 0.8
                right_v *= 0.8
                right_v += v*0.3
                #left_v += v*0.1
                while cnt < 10:
                    #left_v -= v*0.1
                    car.set_speed(right_v, left_v)
                    cnt += 1
                    time.sleep(sample_time*3)         
                obstacle_stop_time = 0
                is_detect = False
                detect_sleep_time = time.time()
                continue
            car.set_speed(0, 0)
            print("Detect obstacle, stop.")
            time.sleep(sample_time)
            continue
        pix_value = share_obj.value
        # print(pix_value,stopSignals, "pix,stop")
        # print(share_ul_obj.value)
        if pix_value > 0:
            stopSignals += 1
        else:
            stopSignals = 0
        
        if stopSignals > 1:
            car.set_speed(0, 0)
            print('red or yellow, stop')
            time.sleep(sample_time)
            if stopSignals > 600:
                stopSignals = 0
                pix_value = 0
            continue

        # delta_v = pid.step(cte, sample_time)
        right_v = left_v = 40
        right, left = inf.detect()
        print(right, left)
        if left == False:
            right_v -= v
            left_v += v
        if right == False:
            right_v += v
            left_v -= v
        print(right_v, left_v)
        car.set_speed(right_v, left_v)

        time.sleep(sample_time)


if __name__ == '__main__':
    main()
