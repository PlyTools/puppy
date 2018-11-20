#!/usr/bin/python
# coding=utf-8

import RPi.GPIO as GPIO
from control.car import Car
from control.car_servo import Car_Servo

class Infrad:
    LEFT = 32       # 设置为左边红外线传感器信号线接到的引脚编号
    RIGHT = 36      # 设置为右边红外线传感器信号线接到的引脚编号

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.LEFT, GPIO.IN)
        GPIO.setup(self.RIGHT, GPIO.IN)

    def detect(self):
        '''
        如果检测到障碍物，就返回False，否则返回True
        '''
        return GPIO.input(self.LEFT), GPIO.input(self.RIGHT)

if __name__ == "__main__":
    inf = Infrad()
    car = Car()
    servo = Car_Servo()

    car.set_duty_cycle(15)      # 15是占空比，决定车速

    try:
        while True:
            left, right = inf.detect()     # 探测有没有遇到障碍物
            print(str(True if left else False) + ", " + str(True if right else False))
            if not left:    # 如果左边检测到障碍物，那就右转，这里我设置舵机为60度，但不确定舵机打60就是右转，
                # detect obstacle on left
                servo.set_angle(60)
            if not right:   # 如果右边检测到障碍物就左转
                # detect obstacle on right
                servo.set_angle(120)
    except KeyboardInterrupt:
        GPIO.cleanup()