import time
import select
import sys
import os
import threading
import RPi.GPIO as GPIO

class Car_Speed:
    #settings
    INA=15; INB=16

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(INA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(INB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    Q=0.25
    R=0.50

    def __init__(self):
        self.measure = 0
        self.count = 0 
        self.lastcount=0
        self.distance=0
        self.speed=0
        
        self.timer=0
        self.x_last=[0, 0, 0]
        self.p_last=1
        

    def __del__(self):
        GPIO.cleanup()

    def callback(self, channel):
        if GPIO.event_detected(self.INA) and self.measure == 1:
            if GPIO.input(self.INB)==0:
                self.count = self.count + 1
            else:
                self.count = self.count - 1
        

    def command(self, measure=0):
        if self.measure == 0 and measure == 1:
            self.measure = measure
            GPIO.add_event_detect(self.INA, GPIO.RISING, callback=self.callback)
            self.timer=threading.Timer(0.1, self.func_speed)
            self.timer.start()
        elif self.measure == 1 and measure == 0:
            self.measure = measure
            GPIO.remove_event_detect(self.INA)
            self.timer.cancel()
            self.count = 0
            self.lastcount=0
            self.distance =0
            self.speed =0
            
    def kalman_filter(self,speed=0):
        #~ x_mid=(self.x_last[2]+speed)*0.5 
        #~ x_now=x_mid
        x_mid=self.x_last[2] 
        p_mid=self.p_last+self.Q 
        kg=p_mid/(p_mid+self.R)
        x_now=x_mid+kg*(speed-x_mid)
        p_now=(1-kg)*p_mid
        
        self.x_last[0]=self.x_last[1]
        self.x_last[1]=self.x_last[2]
        self.x_last[2]=x_now
        self.p_last=p_now
        return  x_now
             
        
    def func_speed(self):
        if self.measure == 1:
            speed = (self.count-self.lastcount)
            self.lastcount = self.count
            self.speed = speed #self.kalman_filter(speed)
            self.timer=threading.Timer(0.1,self.func_speed)
            self.timer.start()

    def get_distance(self):
        if self.measure == 1:
            self.distance  = self.count
        return self.distance

    def get_speed(self):
        return  self.speed


    def test(self):
        print("Please input %s to begin, %s to end, %s, %s to get distance and speed"%('b', 'e', 'd', 's'))
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
                    if c in ['b', 'e', 'd', 's']:
                        if c == "b":
                            self.command(1)
                            print("begin!")
                        elif c == "e":
                            self.command(0)
                            print("end!")                            
                        elif c == "d":
                            distance=self.get_distance()
                            print("distance: %.2f cm"%(distance))
                        elif c == "s":
#                    while True:
                            speed=self.get_speed()
                            print("speed: %.2f cm/s"%(speed))  
                            time.sleep(0.5)    
                                          
        except KeyboardInterrupt:
            self.__del__()
            
          
            
if __name__ == '__main__':
    Car_Speed=Car_Speed()      # Initialize 
    Car_Speed.test()
#    Car_Speed.command(1)      # Start measure, this is always needed
#    speed= Car_Speed.get_speed()       # cm/s, because of Kalman filter, the speed will be stable after  or  seconds.   
#    distance = Car_Speed.get_distance()    # the running distance after encoder.command(1)
#    Car_Speed.command(0)      # Finish measure, this is always needed
    
    
