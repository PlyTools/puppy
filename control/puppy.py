# coding=utf-8

import time
import select
import sys
import os
from threading import Thread
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
    
    def __init__(self):
        self.duty = 0
        self.speed = 0

        self.pid = PID(0.05, 0.1, 0.5)
        self.car = Car()
        self.car_servo = Car_Servo()
        self.ultrasound = Ultrasound()
        self.car_speed = Car_Speed()
        self.car_speed.command(1)      # Start measure, this is always needed
        #args是关键字参数，需要加上名字，写成args=(self,)
        
    
    def keep_speed(self):
        while True:
            print("speed: " + str(self.speed))
            print("real speed: " + str(self.get_speed()))
            err_duty = self.pid.update(self.get_speed() - self.speed)
            print("err_duty: " + str(err_duty))            
            self.duty += err_duty
            if self.duty > 30:
                self.duty = 30
            elif self.duty < -30:
                self.duty = -30
            self.car.set_duty_cycle(self.duty)
            time.sleep(1)

    def set_speed(self, speed):
        if self.speed == 0:
            speed_thread = Thread(target=Puppy.keep_speed, args=(self,))
            speed_thread.start()   
        self.speed = speed

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
    print(puppy.get_speed())
    puppy.set_speed(10)


