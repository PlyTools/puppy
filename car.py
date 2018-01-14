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
    IN1 = 11; IN2 = 12; 
    
    def __init__(self, pwm_hz = 50):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setwarnings(False)
        
        self.PWM_HZ=pwm_hz
        if os.path.exists("./settings.txt") :
            setting = np.loadtxt("./settings.txt")
            self.halfL=setting[0][1]+setting[0][0]*50; self.fullL=setting[0][1]+setting[0][0]*100
            self.halfR=setting[1][1]+setting[1][0]*50; self.fullR=setting[1][1]+setting[1][0]*100
            self.left_duty=50; self.duty=50
            self.leftspeed=self.halfL;self.rightspeed=self.halfR
        else:
            sys.stderr.write('You need to run calibrate first! ')
            self.__del__()
        
        self.pwmIN1 = GPIO.PWM(self.IN1, self.PWM_HZ)
        self.pwmIN2 = GPIO.PWM(self.IN2, self.PWM_HZ)
        self.pwmIN1.start(0)
        self.pwmIN2.start(0)
        
    def __del__(self):
        self.pwmIN1.ChangeDutyCycle(0)
        self.pwmIN2.ChangeDutyCycle(0)
        GPIO.cleanup()
    
    def set_speed(self, speed=90):
        def get_duty(speed):
            '''
            Set right speed of the car
            '''
            if speed > self.fullR:
                speed = self.fullR
            elif speed <-self.fullR:
                speed = -self.fullR
                
            if speed < 0:
                self.duty = -((-speed-self.halfR)*50/(self.fullR-self.halfR)+50);self.rightspeed = speed
            elif speed > 0:
                self.duty = ((speed-self.halfR)*50/(self.fullR-self.halfR)+50);self.rightspeed = speed
            else :
                self.duty = 0; self.rightspeed = 0
        get_duty(speed)
        self.set_duty_cycle(self.duty)
    
    def set_duty_cycle(self, duty = 40):
        '''
        Set duty of the right pwm.
        '''
        self.duty=duty            
        if  self.duty <0 :
            self.pwmIN1.ChangeDutyCycle(0)
            self.pwmIN2.ChangeDutyCycle(-self.duty)
        else :
            self.pwmIN1.ChangeDutyCycle(self.duty)
            self.pwmIN2.ChangeDutyCycle(0)   
          

    def test(self):
        '''
        An realtime control function, help you to test.
        '''
        print("Please input %s, %s and %s to control"%('w', 's', 'q'))
        def click():
            fd = sys.stdin.fileno()
            r = select.select([sys.stdin],[],[])
            rcode = ''
            if len(r[0]) >0:
                rcode  = sys.stdin.read(1)
            return rcode

        try:
            while True:
                c = click()
                if len(c) !=0 :
                    if c in ['w', 's', 'q']:
                        if c == "w":
                            #~ forward = 80
                            #~ self.set_speed(forward)
                            self.set_duty_cycle(80)
                            print("forward")
                        elif c == "s":
                            back = -40
                            self.set_speed(-back)
                            #~ self.set_duty_cycle(-200)
                            print("back")
                        elif c == "q":
                            self.set_speed(0)
                            #~ self.set_duty_cycle(0)
                            print("stop")
                        
        except KeyboardInterrupt:
            self.__del__()

if __name__ == '__main__':
    car = Car()
    car.test()
