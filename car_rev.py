#! /usr/bin/python
# coding=utf-8

import time
import select
import sys
import os
import RPi.GPIO as GPIO
import numpy as np

class Car:
    # settings  
    IN3 = 11; IN4 = 12; IN1 = 15; IN2 = 16
    
    def __init__(self, pwm_hz = 50):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setwarnings(False)
        
        self.PWM_HZ=pwm_hz
        if os.path.exists("./settings.txt") :
            setting = np.loadtxt("./settings.txt")
            self.halfL=setting[0][1]+setting[0][0]*50; self.fullL=setting[0][1]+setting[0][0]*100
            self.halfR=setting[1][1]+setting[1][0]*50; self.fullR=setting[1][1]+setting[1][0]*100
            self.left_duty=50; self.right_duty=50
            self.leftspeed=self.halfL;self.rightspeed=self.halfR
        else:
            sys.stderr.write('You need to run calibrate first! ')
            self.__del__()
        
        self.pwmIN1 = GPIO.PWM(self.IN1, self.PWM_HZ)
        self.pwmIN2 = GPIO.PWM(self.IN2, self.PWM_HZ)
        self.pwmIN3 = GPIO.PWM(self.IN3, self.PWM_HZ)
        self.pwmIN4 = GPIO.PWM(self.IN4, self.PWM_HZ)
        self.pwmIN1.start(0)
        self.pwmIN2.start(0)
        self.pwmIN3.start(0)
        self.pwmIN4.start(0)
        
    def __del__(self):
        self.pwmIN1.ChangeDutyCycle(0)
        self.pwmIN2.ChangeDutyCycle(0)
        self.pwmIN3.ChangeDutyCycle(0)
        self.pwmIN4.ChangeDutyCycle(0)
        GPIO.cleanup()
    
    def set_speed(self, left_speed=90, right_speed=90):
        def get_left_duty(left_speed):
            '''
            Set left speed of the car
            '''
            if left_speed > self.fullL:
                left_speed = self.fullL
            elif left_speed <-self.fullL:
                left_speed = -self.fullL
                
            if left_speed < 0:
                self.left_duty = -((-left_speed-self.halfL)*50/(self.fullL-self.halfL)+50);self.leftspeed = left_speed
            elif left_speed > 0:
                self.left_duty = ((left_speed-self.halfL)*50/(self.fullL-self.halfL)+50); self.leftspeed = left_speed
            else :
                self.left_duty = 0; self.leftspeed = 0

        def get_right_duty(right_speed):
            '''
            Set right speed of the car
            '''
            if right_speed > self.fullR:
                right_speed = self.fullR
            elif right_speed <-self.fullR:
                right_speed = -self.fullR
                
            if right_speed < 0:
                self.right_duty = -((-right_speed-self.halfR)*50/(self.fullR-self.halfR)+50);self.rightspeed = right_speed
            elif right_speed > 0:
                self.right_duty = ((right_speed-self.halfR)*50/(self.fullR-self.halfR)+50);self.rightspeed = right_speed
            else :
                self.right_duty = 0; self.rightspeed = 0
        get_left_duty(left_speed)
        get_right_duty(right_speed)
        self.set_duty_cycle(self.left_duty, self.right_duty)
    
    def set_duty_cycle(self,left_duty = 40, right_duty = 40):
        '''
        Set duty of the pwm.
        '''
        self.left_duty=left_duty
        if self.left_duty <0 :
            self.pwmIN1.ChangeDutyCycle(0)
            self.pwmIN2.ChangeDutyCycle(-self.left_duty)
        else :
            self.pwmIN1.ChangeDutyCycle(self.left_duty)
            self.pwmIN2.ChangeDutyCycle(0) 
        '''
        Set duty of the right pwm.
        '''
        self.right_duty=right_duty            
        if  self.right_duty <0 :
            self.pwmIN3.ChangeDutyCycle(0)
            self.pwmIN4.ChangeDutyCycle(-self.right_duty)
        else :
            self.pwmIN3.ChangeDutyCycle(self.right_duty)
            self.pwmIN4.ChangeDutyCycle(0)   
          

    def test(self):
        '''
        An realtime control function, help you to test.
        '''
        print("Please input %s, %s, %s ,%s and %s to control"%('w', 'a', 's', 'd', 'q'))
        def click():
            fd = sys.stdin.fileno()
            r = select.select([sys.stdin],[],[])
            rcode = ''
            if len(r[0]) >0:
                rcode  = sys.stdin.read(1)
            return rcode
        
        start_itv = 3000.

        try:
            idx = 0
            while True:
                if idx < start_itv:
                   target_v = 80 / start_itv * idx
                   self.set_speed(target_v, target_v)
                else:
                    self.set_speed(int(sys.argv[1]), int(sys.argv[2]))
                idx += 1
                print(idx)
                if idx > int(sys.argv[3]):
                    break
                        
        except KeyboardInterrupt:
            self.__del__()

if __name__ == '__main__':
    car = Car()
    car.test()
