#! /usr/bin/python
# coding=utf-8

# Ultrasound obstacle avoidance

import RPi.GPIO as GPIO
import time

class Ultrasound:
	TRIG = 38
	ECHO = 40
	
	def __init__(self):
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.TRIG, GPIO.OUT,initial=GPIO.LOW)
		GPIO.setup(self.ECHO, GPIO.IN)
		
	def get_distance(self):
		'''
		Get the distance of obstacle
		return 'cm'
		'''
		GPIO.output(self.TRIG, GPIO.HIGH)
		time.sleep(0.000015)
		GPIO.output(self.TRIG, GPIO.LOW)
		while not GPIO.input(self.ECHO):
			pass
		t1 = time.time()
		while GPIO.input(self.ECHO):
			pass
		t2 = time.time()
		return (t2-t1)*34000/2

def ul_main(ul_share_obj, obj_b):
	ul = Ultrasound()
	try:
		while True:
			# print('Distance: %0.2f cm' % ul.get_distance())
                        ul_share_obj.value = ul.get_distance()
                        time.sleep(0.1)
	except KeyboardInterrupt:
		GPIO.cleanup()
# if __name__ == "__main__":
    #  pass
