# coding=utf-8

import time
import select
import sys
import os
from pid import PID
from car import Car
from car_speed import Car_Speed
from car_servo import Car_Servo
from ultrasonic import Ultrasound
import RPi.GPIO as GPIO
import numpy as np

class Puppy:
    # PIN settings  
    IN1 = 12; IN2 = 11
    
    def __init__(self, pwm_hz = 50):
        self.duty = 0
        self.speed = 0

        self.pid = PID(0.1, 0.1, 0.5)
        self.car = Car()
        self.car_servo = Car_Servo()
        self.ultrasound = Ultrasound()
        self.car_speed = Car_Speed()
        self.car_speed.command(1)      # Start measure, this is always needed
    
    def set_speed(self, speed=40, right_speed=40):
        self.speed = speed

        err_duty = self.pid.update(self.get_speed() - speed)
        self.duty += err_duty
        if self.duty > 60:
            self.duty = 60
        elif self.duty < -60:
            self.duty = -60
        self.car.set_duty_cycle(self.duty)

    def get_speed(self):
        return self.car_speed.get_speed()

    def get_obstacal_distance(self):
        return self.ultrasound.get_distance()

    def __del__(self):
        self.car_speed.command(0)
        GPIO.cleanup() 
          
if __name__ == '__main__':
    puppy = Puppy()
    print(puppy.get_obstacal_distance())
    print(puppy.get_speed)
    puppy.set_speed(30)


