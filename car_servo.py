import time
import select
import sys
import os
import RPi.GPIO as GPIO
import numpy as np

class Car_Servo:
    #settings
    PINOUT = 18
    
    PinHz  = 50
    DutyMin = 2.72
    DutyMax = 12
    
    def __init__(self, angle = 90): #    angle = 0~180;
        self.angle   = angle
        self.pinduty = (self.angle/180.0)*(self.DutyMax-self.DutyMin)+self.DutyMin

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PINOUT, GPIO.OUT)
        GPIO.setwarnings(False)
        self.PINOUT = GPIO.PWM(self.PINOUT, self.PinHz)
        self.PINOUT.start(self.pinduty)
        
    def __del__(self):
        GPIO.cleanup()
        
    def set_angle(self, angle):
        if angle>180:
            angle = 180
        elif angle < 0:
            angle = 0
        self.angle   = angle
        self.pinduty = (self.angle/180.0)*(self.DutyMax - self.DutyMin) + self.DutyMin
        self.PINOUT.ChangeDutyCycle(self.pinduty)
        #time.sleep(5)
        #self.PINOUT.ChangeDutyCycle(0)
        
    def test(self):
        ang=90
        print("Please input %s to add 5*,and %s to decrease 5*:"%('a', 'd'))
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
                    if c in ['a', 'd']:
                        if c == "a":
                            ang=ang+5;
                        elif c == "d":
                            ang=ang-5;
                        if ang>180:
                            ang = 180
                        elif ang < 0:
                            ang = 0        
                        self.set_angle(ang)
                        print("ang = %d "%ang)
                    
                        
        except KeyboardInterrupt:
            self.__del__()

if __name__ == '__main__':
    servo= Car_Servo()
    servo.test()
