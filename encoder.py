#! /usr/bin/python
# coding=utf-8

import time
import select
import sys
import os
import threading
import RPi.GPIO as GPIO

class Encoder:
    #settings
    INleft=35; INright=37
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(INleft, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(INright, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    Q=0.25
    R=0.50

    def __init__(self):
        self.measure = 0
        self.count_left = 0
        self.count_right = 0
        self.lastcount_left=0
        self.lastcount_right=0
        self.distance_left =0
        self.distance_right =0
        self.speed_left =0
        self.speed_right =0
        self.timer=0
        self.x_lastleft=[0, 0, 0]
        self.x_lastright=[0, 0, 0]
        self.p_lastleft=1
        self.p_lastright=1
        

    def __del__(self):
        GPIO.cleanup()

    def callback_left(self, channel):
        if GPIO.event_detected(self.INleft) and self.measure == 1:
            self.count_left = self.count_left + 1
        
    def callback_right(self, channel1):
        if GPIO.event_detected(self.INright) and self.measure == 1:
            self.count_right  = self.count_right  + 1

    def command(self, measure=0):
        if self.measure == 0 and measure == 1:
            self.measure = measure
            GPIO.add_event_detect(self.INleft, GPIO.RISING, callback=self.callback_left)
            GPIO.add_event_detect(self.INright, GPIO.RISING, callback=self.callback_right)
            self.timer=threading.Timer(0.1, self.func_speed)
            self.timer.start()
        elif self.measure == 1 and measure == 0:
            self.measure = measure
            GPIO.remove_event_detect(self.INleft)
            GPIO.remove_event_detect(self.INright)
            self.timer.cancel()
            self.count_left = 0
            self.count_right = 0
            self.lastcount_left=0
            self.lastcount_right=0
            self.distance_left =0
            self.distance_right =0
            self.speed_left =0
            self.speed_right =0
            
    def kalman_filter(self,speed=0, left_or_right="left"):
        #~ x_mid=(self.x_lastleft[2]+speed)*0.5 if left_or_right=="left" else (self.x_lastright[2]+speed)*0.5
        #~ x_now=x_mid
        x_mid=self.x_lastleft[2] if left_or_right=="left" else self.x_lastright[2]
        p_mid=self.p_lastleft+self.Q if left_or_right=="left" else self.p_lastright+self.Q
        kg=p_mid/(p_mid+self.R)
        x_now=x_mid+kg*(speed-x_mid)
        p_now=(1-kg)*p_mid
        if left_or_right=="left":
            self.speed_left=x_now
            self.x_lastleft[0]=self.x_lastleft[1]
            self.x_lastleft[1]=self.x_lastleft[2]
            self.x_lastleft[2]=x_now
            self.p_lastleft=p_now
        else :
            self.speed_right=x_now
            self.x_lastright[0]=self.x_lastright[1]
            self.x_lastright[1]=self.x_lastright[2]
            self.x_lastright[2]=x_now
            self.p_lastright=p_now                 
        
    def func_speed(self):
        if self.measure == 1:
            speed_left = 1.052*(self.count_left-self.lastcount_left)*2.5
            self.lastcount_left = self.count_left 
            speed_right = 1.052*(self.count_right-self.lastcount_right)*2.5
            self.lastcount_right = self.count_right
            self.kalman_filter(speed=speed_left, left_or_right="left")
            self.kalman_filter(speed=speed_right, left_or_right="right")
            self.timer=threading.Timer(0.4,self.func_speed)
            self.timer.start()

    def get_distance(self):
        if self.measure == 1:
            self.distance_left  = 1.052*self.count_left
            self.distance_right = 1.052*self.count_right
        return self.distance_left, self.distance_right

    def get_speed(self):
        '''
        Get the speed of car
        '''
        return  self.speed_left, self.speed_right


    def test(self):
        print("Please input %s to start, %s to stop, %s, %s to get distance and speed"%('q', 'w', 'e', 'r'))
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
                    if c in ['q', 'w', 'e', 'r']:
                        if c == "q":
                            self.command(1)
                            print("start!")
                        elif c == "w":
                            self.command(0)
                            print("stop!")                            
                        elif c == "e":
                            left_distance, right_distance=self.get_distance()
                            print("left_distance: %.2f cm, right_distance: %.2f cm"%(left_distance,right_distance))
                        elif c == "r":
                            while True:
                                left_speed, right_speed=self.get_speed()
                                time.sleep(0.4)
                                print("left_speed: %.2f cm/s, right_speed: %.2f cm/s"%(left_speed,right_speed))                
        except KeyboardInterrupt:
            self.__del__()
            
          
            
if __name__ == '__main__':
    encoder= Encoder()      # Initialize Encoder
    encoder.command(1)      # Start measure, this is always needed
    left, right = encoder.get_speed()       # cm/s, because of Kalman filter, the speed will be stable after 3 or 4 seconds.   
    left, right = encoder.get_distance()    # the running distance after encoder.command(1)
    encoder.command(0)      # Finish measure, this is always needed
    
    
