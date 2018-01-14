#!/usr/bin/python  
# coding=utf-8  
 
import RPi.GPIO as GPIO  
import time  
import sys  

class Infrad:
	LEFT = 32
	RIGHT = 36
	
	def __init__(self):
		GPIO.setwarnings(False)   
		GPIO.setmode(GPIO.BOARD)  
		GPIO.setup(self.LEFT,GPIO.IN)
		GPIO.setup(self.RIGHT,GPIO.IN)
	
	def detect(self):
		'''
		If it detect the obstacle, return False, otherwise True.
		'''
		return GPIO.input(self.LEFT), GPIO.input(self.RIGHT)

if __name__ == "__main__":
	inf = Infrad()
	try:
		while True:
			left, right = inf.detect()
			print(str(True if left else False) + ", " + str(True if right else False))
	except KeyboardInterrupt:
		GPIO.cleanup()
