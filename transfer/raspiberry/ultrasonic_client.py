# -*- coding: utf-8 -*-

from socket import *
import RPi.GPIO as GPIO
import time

host=('192.168.1.100', 8002)

class Ultrasound:
	TRIG = 38
	ECHO = 40
	
	def __init__(self):
		GPIO.setwarnings(False)
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

def distanceStream(ultra):
    # create a socket and bind socket to the host
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(host)
    try:
        while True:
            # send data to the host every 0.5 sec
            print("measure distance")
            distance = ultra.get_distance()
            print("Distance : %.1f cm" % distance)
            client_socket.send(str(distance).encode())
            time.sleep(0.5)
    except KeyboardInterrupt:
        client_socket.close()
        GPIO.cleanup
    finally:
        client_socket.close()
        GPIO.cleanup()

if __name__=="__main__":
    ultra=Ultrasound()
    distanceStream(ultra)
